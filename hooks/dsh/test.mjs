import assert from 'node:assert/strict'
import { apply, gateText } from './index.js'

const at = (hour, minute) => Date.UTC(2026, 8, 7, hour - 9, minute)
const missing = new URL('./missing-policy.md', import.meta.url)

for (const [hour, minute, active] of [[21, 29, false], [21, 30, true], [0, 0, true], [4, 59, true], [5, 0, false]]) {
  const text = gateText(at(hour, minute))
  assert.match(text, active ? /GATE=ACTIVE/ : /GATE=INACTIVE/)
  assert.equal(text.includes('# Evening Exploration Policy'), active)
  assert.equal(text.includes('DeepSeek'), active)
}
assert.match(gateText(at(23, 0)), /Asia\/Tokyo: 2026-09-07T23:00\+09:00/)
assert.throws(() => gateText(at(23, 0), missing), { code: 'ENOENT' })
gateText(at(12, 0), missing)

let listener
apply({ on: (event, fn) => { assert.equal(event, 'agent/pre-step'); listener = fn } })
const step = (messages) => listener({}, async () => ({ kind: 'enter', messages }))
const human = { role: 'user', source: { kind: 'user', rpcId: 'r1' } }
const parent = { role: 'user', source: { kind: 'user' } }

const injected = (await step([human])).messages
assert.equal(injected.length, 2)
assert.equal(injected[1].source.kind, 'evening-exploration')
assert.match(injected[1].content[0].text, /EVENING_EXPLORATION_GATE=/)
assert.equal((await step([parent])).messages.length, 1)
assert.deepEqual(await listener({}, async () => ({ kind: 'reject' })), { kind: 'reject' })
console.log('ok')
