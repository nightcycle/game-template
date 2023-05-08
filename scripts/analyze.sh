luau-lsp analyze src \
--sourcemap=sourcemap.json \
--ignore="Packages/**" \
--ignore="out/**" \
--definitions=types/globalTypes.d.lua \
> src_analysis.txt 2>&1
echo "src errors remaining: $(wc -l < src_analysis.txt)"

# luau-lsp analyze out \
# --sourcemap=sourcemap.json \
# --ignore="Packages/**" \
# --definitions=types/globalTypes.d.lua \
# > out_analysis.txt 2>&1
# echo "out errors remaining: $(wc -l < out_analysis.txt)"

# luau-lsp analyze Packages \
# --ignore="**.spec.**" \
# --sourcemap=sourcemap.json \
# --definitions=types/globalTypes.d.lua \
# --no-strict-dm-types \
# > package_analysis.txt 2>&1
# echo "package errors remaining: $(wc -l < package_analysis.txt)"

# selene src >> analysis.txt
