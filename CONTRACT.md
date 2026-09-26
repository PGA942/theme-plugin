# RASQ スロットプラグイン契約 — 正典は rasq-sdk-sample

この文書は **`rasq-sdk-sample/docs/slots.md`** にある(v0.8 から各リポジトリの `CONTRACT.md` はこのポインタだけ)。
このリポジトリ(着せ替え = `kind: "theme"`)に関わるのは **§2.12**(v0.16)と、画像の形式・上限を共有する §2.10(アセットパック)。

- 契約の本文(§1 マニフェスト / §2.1〜2.12 スロット別とパック / §3 RRL のホスト拡張 / §4 ホスト関数 / §5 ホスト側の読み込み):
  https://gitlab.com/orgate-question/rasq-sdk-sample/-/blob/main/docs/slots.md — **節番号は同じ**(README の「§2.x」はそのまま読める)
- マニフェスト: `rasq-sdk-sample/schema/manifest.schema.json`(`$defs.theme` / `themeColors` / `themeSurface` / `themeLayer`)。
  配布物の目次: `schema/bundle.schema.json`(root.kind = theme は wasm 無し)
- 検証: `python3 schema/validate.py`(`examples/manifests/sample.theme-starry.json` がこのサンプルのマニフェストと同じもの)
