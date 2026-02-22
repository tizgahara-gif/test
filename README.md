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

- 1回押すごとにオブジェクトを3つ作成（専用関数ではなく Blender の追加オペレーター（Add）で生成）:
  - `hair`（Bézier Curve、アクティブコレクション直下）
  - `taper`（Bézier Curve、`taper` コレクション直下）
  - `bavel`（**Bézier Circle**、`bevel` コレクション直下）
- `taper` / `bevel` コレクションが無い場合は新規作成、既にある場合は再利用して直下へ配置
- `taper` / `bevel` コレクションを新規作成する場合、コレクションアイコン色を緑（`COLOR_04`）に設定
- 追加した `hair` の Curve Geometry に、追加した `taper` を Taper Object として設定
- 追加した `hair` の Curve Bevel Mode を `Object` にし、追加した `bavel`（Bézier Circle）を Bevel Object として設定
- `hair1` など連番付き Hair 生成時、同じ連番の `taper1` / `bevel1`（または `bavel1`）が既にあれば新規生成せず既存オブジェクトを再利用
- `hair1` 生成時に `taper` / `bevel` が存在しない場合は、`taper1` / `bevel1` を同時生成し、Geometry/Bevel へ割り当て
- `hair2` 生成時に `taper2` / `bevel2` が無ければ、その番号で新規生成して割り当て
- `OtG` ボタンで、現在選択中オブジェクトの Origin を Geometry へ移動
- 既に同名オブジェクトが存在する場合は、末尾に連番を付けて作成:
  - 例: `hair`, `hair1`, `hair2` ...

## カスタマイズ

- タブ名は `TAB_NAME` を変更
- 作成対象名は `BASE_OBJECT_NAMES` を変更
- コレクション振り分けは `COLLECTION_BY_BASE_NAME` を変更
- 生成オペレーターは `bpy.ops.curve.primitive_bezier_curve_add` / `bpy.ops.curve.primitive_bezier_circle_add` を変更
