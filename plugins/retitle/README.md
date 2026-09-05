# Chat Title Naming

ChatGPT と Codex で同じ命名ルールを使うための、skills-only plugin です。
会話を要約するのではなく、数か月後に一覧から見たときに思い出せる短い
タイトルを提案します。

この plugin は外部サービス、MCP server、認証、独自 UI を持ちません。
タイトルを提案するだけで、既存のチャット名を自動変更することも、Side
Chat を自動で開くこともありません。

## 構成

~~~text
retitle/
├── .codex-plugin/plugin.json
├── README.md
├── skills/
│   └── retitle/
│       ├── SKILL.md
│       └── agents/openai.yaml
└── submission/
    └── test-cases.md
~~~

命名ルールの唯一の正本は skills/retitle/SKILL.md です。Codex
用の standalone skill を使う場合も、このフォルダをそのままコピーして
ください。別の SKILL.md を複製して二重管理しないでください。

## ChatGPT Web で使う

ChatGPT Web ではローカルのフォルダを直接読み込ませることはできません。
公開または workspace 配布した plugin を ChatGPT Work で有効にする形です。

1. OpenAI Platform の Plugin submission portal で Create plugin を選び、
   submission type は Skills only にします。
2. この plugin の skills/retitle フォルダを最終 skill bundle
   としてアップロードします。ポータルが archive を求める場合は、この
   skill フォルダを ZIP 化します。
3. 公開用の developer identity、website、support URL、privacy policy、
   terms、logo、地域設定をポータルで用意します。これらは個人ごとに異なる
   ため、この source package には仮の値を入れていません。
4. submission/test-cases.md の 5 件の positive test と 3 件の negative
   test をポータルの Testing に転記します。
5. Review 後に Publish します。ChatGPT Web では Work chat を新規作成し、
   composer の @ からこの plugin を選んで title を依頼します。

公開後は ChatGPT と Codex の共通 Plugins Directory から利用できます。
公開せず workspace 内だけで使いたい場合は、workspace admin による
plugin 配布権限と、その workspace の plugin policy が必要です。

## Codex で使う

standalone skill として使うなら、skills/retitle を
CODEX_HOME/skills/retitle、または通常は
~/.codex/skills/retitle にコピーします。

agents/openai.yaml の allow_implicit_invocation は false です。通常の作業中に
自動発火せず、$retitle を明示 invocation したときだけ命名ルールを
読み込みます。

plugin として Codex に配布したい場合は、この plugin root を personal または
repo marketplace に登録してください。marketplace は local development 用であり、
ChatGPT Web へローカルフォルダを直接インストールする方法ではありません。

## 公開前の確認

~~~text
python -X utf8 <plugin-creator>/scripts/validate_plugin.py <plugin-root>
python -X utf8 <skill-creator>/scripts/quick_validate.py <skill-folder>
~~~

公開前には manifest の author と interface の developerName を、Platform で
検証済みの publisher identity と一致させてください。また、plugin submission
では Apps Management の Write 権限が必要です。

仕様の参照先:

- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [Build skills](https://developers.openai.com/plugins/build/skills)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission)
