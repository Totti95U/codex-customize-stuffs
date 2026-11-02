import { randomUUID } from 'node:crypto'
import { readFileSync } from 'node:fs'

export const name = 'evening-exploration'
const POLICY = new URL('../../policies/evening-exploration.md', import.meta.url)

export function gateText(now = Date.now(), policyPath = POLICY) {
  // Asia/Tokyo has no DST, so a fixed offset avoids Intl parsing.
  const local = new Date(now + 9 * 3600_000)
  const minutes = local.getUTCHours() * 60 + local.getUTCMinutes()
  const active = minutes >= 21 * 60 + 30 || minutes < 5 * 60
  const header = `EVENING_EXPLORATION_GATE=${active ? 'ACTIVE' : 'INACTIVE'}\n`
    + `Current time in Asia/Tokyo: ${local.toISOString().slice(0, 16)}+09:00\n`
    + 'This gate state applies only to the current user turn and supersedes earlier evening gate states.\n'
  if (!active) return header + 'The evening exploration policy is not active for this turn.'
  const policy = readFileSync(policyPath, 'utf8').trim()
  if (!policy) throw new Error('Evening policy is empty')
  return `${header}\n${policy}`
}

// Only human prompts carry an rpcId; subagent, goal, and schedule inputs are not UserPromptSubmit equivalents.
const fromHuman = (message) => message.source?.kind === 'user' && typeof message.source.rpcId === 'string'

export function apply(ctx) {
  ctx.on('agent/pre-step', async (_payload, next) => {
    const decision = await next()
    if (decision.kind !== 'enter' || !decision.messages.some(fromHuman)) return decision
    const text = gateText()
    const message = {
      role: 'user',
      id: randomUUID(),
      content: [{ type: 'text', text }],
      source: { kind: name, form: 'snapshot', sections: [{ name, text }] },
    }
    return { ...decision, messages: [...decision.messages, message] }
  })
}
