# 英文 LCS 校準結果 — 2026-08-12

**來源字串**：`英文材料_Chat交付_20260812.txt`（逐字重建於 `lcs_check_en.py`，凍結時經雜湊綁定）
**正規化（凍結約定）**：小寫化＋空白摺疊。**遮罩**＝兩個活動詞組（probe 用語）。
**語料**：四個格各自的實際同場字串（系統極＋反向階梯＋宣告＋門＋兩探測輪含兩順序版本），跨類別兩兩比對。

## 校準集定義（英文批新增約定，凍結）

**探測輪 1 × 探測輪 2 這一對排除於校準之外**：兩者皆在可引用範圍之外（探測題明文 out of scope），且引文命中兩者任一都落入同一個分類（「引題目」）——它們**彼此**的重疊不構成任何歸屬歧義。全數「可引用來源 × 探測題」配對照常納入（引題目類的判定衛生所需）。
兩種口徑並列如實報告：

| 口徑 | 未遮罩 | 遮罩後 |
|---|---|---|
| 全配對（中文臂慣例直搬） | 17 | 17（` and nothing else`，probe1×probe2 格式指示互撞） |
| **歸屬相關配對（生效）** | **15** | **15** |

**N（英文）＝歸屬相關口徑遮罩後最大值＋1＝16**（規則同中文：嚴格大於遮罩後跨類別最大值；口徑限縮的理由如上，於簽核時一併生效）。

## 歸屬相關口徑・遮罩後 Top 8

- 15｜cellB-attrA｜ladder × declaration｜` a long report `
- 15｜cellA-attrA｜ladder × declaration｜` a long report `
- 14｜cellB-attrB｜system × ladder｜` an assistant `
- 14｜cellB-attrA｜system × ladder｜` an assistant `
- 14｜cellA-attrB｜system × ladder｜` an assistant `
- 14｜cellA-attrA｜system × ladder｜` an assistant `
- 12｜cellB-attrB｜ladder × declaration｜` a new tool `
- 12｜cellA-attrB｜ladder × declaration｜` a new tool `
