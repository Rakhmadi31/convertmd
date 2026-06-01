-- Lua filter for Pandoc: convert Markdown tables to LaTeX tabularx tables
-- so that long text in cells wraps when generating PDF.

function Meta(meta)
  if FORMAT:match("latex") then
    local includes = meta["header-includes"] or {}
    if type(includes) == "string" then
      includes = {includes}
    end

    table.insert(includes, 1, pandoc.RawBlock("latex", [[\usepackage{booktabs}\usepackage{tabularx}\usepackage{array}\usepackage{ragged2e}\newcolumntype{L}{>{\RaggedRight\arraybackslash}X}]]))
    if not meta["header-includes"] then
      meta["header-includes"] = includes
    else
      meta["header-includes"] = includes
    end
  end
  return meta
end

local function align_spec(align)
  if align == "AlignRight" then
    return ">{\\RaggedLeft\\arraybackslash}X"
  elseif align == "AlignCenter" then
    return ">{\\Centering\\arraybackslash}X"
  else
    return "L"
  end
end

local function render_cell(cell)
  local content = cell.contents or cell.blocks or cell[5] or cell[2] or cell
  local doc = pandoc.Pandoc(content)
  local latex = pandoc.write(doc, "latex")
  latex = latex:gsub("\n", " ")
  latex = latex:gsub("%s+$", "")
  return latex
end

local function row_cells(row)
  if row.cells then
    return row.cells
  elseif row[4] then
    return row[4]
  elseif row[3] then
    return row[3]
  elseif row[2] then
    return row[2]
  elseif row[1] and type(row[1]) == "table" and #row == 2 then
    return row[1]
  end
  return row
end

local function render_row(row)
  local cells = {}
  for _, cell in ipairs(row_cells(row)) do
    table.insert(cells, render_cell(cell))
  end
  return table.concat(cells, " & ")
end

local function section_rows(section)
  if not section then
    return {}
  end
  if section[1] and section[1].cells then
    return section
  elseif section[2] and type(section[2]) == "table" then
    return section[2]
  end
  return section
end

function Table(tbl)
  if not FORMAT:match("latex") then
    return tbl
  end

  local alignments = {}
  local header_rows = {}
  local body_rows = {}
  local caption

  if tbl.colspecs then
    for _, colspec in ipairs(tbl.colspecs) do
      table.insert(alignments, align_spec(colspec.align))
    end
  end

  if tbl.head then
    header_rows = tbl.head.rows or {}
  elseif tbl.headers then
    header_rows = tbl.headers or {}
  end

  if tbl.bodies and tbl.bodies[1] then
    body_rows = tbl.bodies[1].body or {}
  elseif tbl.rows then
    body_rows = tbl.rows or {}
  end

  caption = tbl.caption

  local header = {}
  if caption and #caption > 0 then
    local caption_text = pandoc.utils.stringify(caption)
    if caption_text ~= "" then
      table.insert(header, string.format("\\caption*{%s}", caption_text))
    end
  end

  table.insert(header, string.format("\\begin{tabularx}{\\textwidth}{%s}", table.concat(alignments, "")))
  table.insert(header, "\\toprule")

  if #header_rows > 0 then
    table.insert(header, render_row(header_rows[1]) .. [[ \\ ]])
    table.insert(header, "\\midrule")
  end

  for _, row in ipairs(body_rows) do
    table.insert(header, render_row(row) .. [[ \\ ]])
  end

  table.insert(header, "\\bottomrule")
  table.insert(header, "\\end{tabularx}")

  return pandoc.RawBlock("latex", table.concat(header, "\n"))
end
