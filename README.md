# Simple_hair5 (Blender 5.x)

Blender 5.x 向けの最小構成アドオンです。以下を含みます。

- `bl_info`（Blender 5.0.0 指定）
- `Panel` 1つ（**3D View > Nパネル > SH5** に表示）
- `Operator` 1つ（ボタン押下で `hair` / `taper` / `bavel` を作成）
- `register()` / `unregister()`

## ファイル構成

```text
minimal_blender5_addon/
  └─ __init__.py
```

## 使い方

1. `minimal_blender5_addon` フォルダを zip 化する。
2. Blender で `Edit > Preferences > Add-ons > Install...` から zip を選ぶ。
3. Add-on を有効化する。
4. `3D View` で `N` キーを押し、`SH5` タブを開く。
5. `SH5` パネルの `Create hair/taper/bavel` ボタンを押す。

## ボタン動作

- 1回押すごとにオブジェクトを3つ作成:
  - `hair`（Bézier Curve、アクティブコレクション直下）
  - `taper`（Bézier Curve、`taper` コレクション直下）
  - `bavel`（**Bézier Circle**、`bevel` コレクション直下）
- `taper` / `bevel` コレクションが無い場合は新規作成、既にある場合は再利用して直下へ配置
- 追加した `hair` の Curve Geometry に、追加した `taper` を Taper Object として設定
- 追加した `hair` の Curve Bevel Mode を `Object` にし、追加した `bavel`（Bézier Circle）を Bevel Object として設定
- 既に同名オブジェクトが存在する場合は、末尾に連番を付けて作成:
  - 例: `hair`, `hair1`, `hair2` ...

## カスタマイズ

- タブ名は `TAB_NAME` を変更
- 作成対象名は `BASE_OBJECT_NAMES` を変更
- コレクション振り分けは `COLLECTION_BY_BASE_NAME` を変更
- Curve 形状は `create_bezier_curve_object()` / `create_taper_bezier_object()` / `create_bezier_circle_object()` を変更
- `taper` は専用関数 `create_taper_bezier_object()` で Bézier Curve を生成
