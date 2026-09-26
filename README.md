# theme-plugin — 着せ替え(テーマ)パックのサンプル「星空」「RASQ」(`kind: "theme"`)

アプリの見た目を変える**着せ替え**のサンプルを 2 つ置いたワークスペース。どちらも wasm を持たない配布物で、
中身はマニフェストの `theme`(宣言)と画像だけ。ホストは宣言を読むだけで、コードは動かない / 権限も無い。

| パック | id | 版 | 見どころ |
|---|---|---|---|
| `packs/starry/`「星空」 | `sample.theme-starry` | 0.1.0 | 画像のレイヤー(背景 / 上に重ねる星の粒 / ボタン)、色、アイコンの差し替え(契約 v0.16) |
| `packs/rasq/`「RASQ」 | `sample.theme-rasq` | 0.1.0 | グラデーションのレイヤー、辺に寄せた帯(`height`)、面の文字色(`onColor`)(契約 v0.17) |

## 「星空」(`sample.theme-starry`)

- 背景: メインの画面(`app`)と FOW(下から出るパネル、`fow`)に夜空の絵(紺 → 藍のグラデーション + 薄い天の川)
- 投稿タイル(`postTile`): 半透明の紺に角丸 12、**上に**星の粒を敷き詰めて重ねる(`position: "above"`、`repeat`)
- アクションバーのボタン(`actionButton`): 藍色のにじみを背景に、角丸 18
- いいねのアイコン(`favorite_border`)を淡い黄色の星に、リポストのアイコン(`repeat`)を Material の `autorenew` に差し替え
- 色: 暗いテーマ用に `primary` / `surface` / `onSurface` / `outline`、明るいテーマ用に `primary` だけ。
  `brightness: "dark"` なので、アプリが明るい設定のときは色と面の宣言を使わない(アイコンの差し替えだけ効く)

## 「RASQ」(`sample.theme-rasq`、v0.17)

投稿タイルと FOW だけを変える控えめな着せ替え。画像は薄い RASQ のマーク 1 枚で、あとはグラデーション。

- 投稿タイル(`postTile`): 右寄せの薄い RASQ のマーク(`asset: "mark"`、`fit: "contain"`、`alignment: "centerRight"`)の上に、
  上辺に寄せた高さ 28 の**帯**(`gradient` の `#1F1E33` → `#001F1E33`、`alignment: "topCenter"`、`height: 28`)。
  `#001F1E33` は同じ色の不透明度 0 なので、帯は下に向かって投稿の背景色に溶ける
- FOW(`fow`): `#02775C` → `#178178` の縦の緑のグラデーション(`begin: "topCenter"`、`end: "bottomCenter"`)に、
  文字とアイコンは白(`onColor: "#FFFFFF"`)
- `brightness: "both"`(明るい設定でも暗い設定でも効く)。`colors` / `icons` は書いていない
- マークの画像 `theme/rasq_mark_faded.png` は rasq-client の `packages/rasq_design/assets/brand/rasq_icon.png`(透過 PNG、402×400)の
  不透明度を 0.12 倍にしたもの(`tools/make_images.py` が作る)

レイヤーは `asset`(画像)か `gradient`(グラデーション)のどちらか 1 つ。`gradient` = `colors`(2〜8 個)/ `stops`(省略 = 等間隔。
書くなら `colors` と同じ数で昇順)/ `begin` / `end`。`height`(1〜400)を書くと面いっぱいではなく `alignment` の辺に寄せた帯になる
(`top*` = 上辺、`bottom*` = 下辺、`center*` = 真ん中)。`fit` / `repeat` は画像のときだけ意味がある。

## このリポジトリの形(`rasq` ワークスペース)

`rasq-sdk-sample` の `docs/cli.md` §2 のワークスペース。`rasq init --namespace sample`、
`rasq new theme starry --id sample.theme-starry --display 星空`、`rasq new theme rasq --id sample.theme-rasq --display RASQ` が作る形に、
画像とマニフェストを入れたもの(雛形の `theme/background.png` はどちらも使わないので消してある)。

```
rasq.toml                     # schema = "rasq.workspace/1"、[[packs]] に starry(sample.theme-starry)と rasq(sample.theme-rasq)
Cargo.toml / kit/             # rasq init が作る(このリポジトリには Rust のプラグインが無いので使わない)
packs/starry/
  manifest.json               # kind = "theme"。assets(use = "theme")と theme(colors / icons / surfaces)
  theme/sky.png               # 1080×1920 夜空(app / fow の背景)
  theme/stars.png             # 256×256 透過の星の粒(継ぎ目なしのタイル。postTile に above で重ねる)
  theme/button.png            # 96×96 透過の藍色のにじみ(actionButton の背景)
  theme/heart.png             # 128×128 透過の淡い黄色の星(favorite_border の差し替え)
packs/rasq/
  manifest.json               # kind = "theme"。postTile(マーク + 上辺の帯)と fow(グラデーション + onColor)
  theme/rasq_mark_faded.png   # 402×400 透過の RASQ のマーク(不透明度 0.12 倍)
tools/make_images.py          # 上の 5 枚を Pillow で作る(星空はシード固定、RASQ は元の絵から。何度走らせても同じ画像)
dist/                         # rasq build の出力(.rasqpkg)
```

- 契約の正典は [`CONTRACT.md`](CONTRACT.md) が指す `rasq-sdk-sample/docs/slots.md` §2.12(画像の形式と上限は §2.10 と共通)。
- `theme` の中身(「星空」の場合):

| キー | このサンプル | 意味 |
|---|---|---|
| `brightness` | `dark` | どちらの明るさで効くか(`light` / `dark` / `both`、既定 `both`) |
| `colors.dark` / `colors.light` | `primary` など | Material の ColorScheme の上書き。色は `#RRGGBB` か `#AARRGGBB`(8 桁は**先頭**が不透明度。`#CC0B1026` = `#0B1026` の 80%) |
| `icons` | `favorite_border` → `asset:heart`、`repeat` → `material:autorenew` | 名前で持っているアイコンの差し替え |
| `surfaces.app` / `fow` / `postTile` / `actionButton` | `color` / `radius` / `layers` | 面ごとの塗り / 角丸(0〜48)/ 重ねる画像(最大 8 枚) |

`layers[]` は `asset`(`assets[].id`、`use: "theme"` のもの)か `gradient`(v0.17)/ `position`(`below` = 背景、`above` = 中身の上。
**above は触れない**)/ `fit` / `alignment` / `repeat` / `opacity` / `height`(v0.17、帯)。面には `onColor`(v0.17、文字とアイコンの色)も書ける。

## 画像を作り直す

```sh
pip3 install pillow
python3 tools/make_images.py   # packs/starry/theme/ の 4 枚と packs/rasq/theme/ の 1 枚を上書き(大きさも出す)
python3 tools/make_images.py --rasq-icon <path>/rasq_icon.png   # RASQ のマークの元が隣の rasq-client に無いとき
```

元の `rasq_icon.png` が見つからなければ RASQ のマークは作らずに飛ばす(星空の 4 枚は作る)。
どれも 1 枚 2 MiB・合計 16 MiB の上限よりずっと小さい(星空 90 KB 弱、RASQ 12 KB)。絵を差し替えるときは、同じパスに置けば
マニフェストはそのまま使える。画像を足すなら `assets` に `use: "theme"` で書き、`surfaces` か `icons` から指す。

## ビルドと確認

`rasq` CLI は `rasq-sdk-sample` から組む(`cd rust && cargo build --release -p rasq-cli`)。
Rust のプラグインが無いワークスペースなので、wasm のビルドも `cargo test` も走らない。

```sh
rasq check                     # スキーマ / 画像の形式(マジックナンバー)と大きさ / 書き忘れ / 参照の整合
rasq build --raw               # dist/sample.theme-starry-0.1.0.rasqpkg と dist/sample.theme-rasq-0.1.0.rasqpkg(パックごとに 1 つ。wasm 無しなので生の .wasm は出ない)
rasq inspect dist/sample.theme-starry-0.1.0.rasqpkg   # root: sample.theme-starry 0.1.0 (theme)、asset 4 枚
rasq inspect dist/sample.theme-rasq-0.1.0.rasqpkg     # root: sample.theme-rasq 0.1.0 (theme)、asset 1 枚
```

`rasq check` の整合: `surfaces.*.layers[].asset` と `icons` の `asset:<id>` が `assets` に `use: "theme"` で載っていること
(無ければ error)、`gradient.stops` が `colors` と同じ数で昇順であること(error)、どこからも指されていない画像
(配布物には入るが使われない)とグラデーションに書いた `fit` / `repeat` は warning。色の形・面のキー・`layers` の数・
`asset` と `gradient` のどちらか 1 つ はスキーマが見る。

## ホストでの効き方(rasq-client)

1. ストアからインストールすると(`rasq publish` のカテゴリは `theme`)、画像が端末に保存される。
2. **設定 → アプリの外観 → フォントやカラースキーム** に「星空」「RASQ」が並ぶ。選ぶと効く。**同時に有効にできる着せ替えは 1 つ**
   (別のものを選ぶと前のものは外れる)。
3. アプリが暗い設定のとき: 色が差し替わり、メインの画面と FOW の背景が夜空に、投稿タイルに星の粒が重なり、
   アクションバーのボタンに藍色のにじみが付く。星の粒(`above`)は描くだけでタッチを通すので、タイルの押せる部分はそのまま押せる。
4. アイコンの差し替え(いいね = 星、リポスト = `autorenew`)は明るさに関わらず効く。
5. 「RASQ」を選ぶと(明暗どちらでも): 投稿タイルの上辺に下へ溶ける帯と右寄せの薄いマーク、FOW は緑のグラデーションに白い文字。

ホストは配布物に wasm が 1 つでも入っていたら着せ替えとして扱わない。

## 掲載(審査)に出す

`rasq build` が出す `dist/sample.theme-starry-0.1.0.rasqpkg` / `dist/sample.theme-rasq-0.1.0.rasqpkg` がそのまま掲載できる形
(zstd tar + `bundle.json` `rasq.bundle/1` の root = `{id, version, kind: "theme", manifest}` + `SHA512SUMS`)。
`rasq publish --central <url> --dry-run` で Central への要求を書き出せる。審査は画像の内容と権利の確認だけ。
開発者鍵の署名(`*.sig.json`)はサイドロード用で、リポジトリには入れない。
