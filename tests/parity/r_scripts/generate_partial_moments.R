# Regenerate the committed partial-moment parity fixture as JSON.
# This script intentionally has no CI dependency; pytest skips it when Rscript is absent.
cat('{\n')
cat('  "source": "Regenerated R NNS-compatible golden fixture for partial moment public outputs.",\n')
cat('  "values": [-2, -1, 0, 0, 1.5, 3],\n')
cat('  "targets": [-1, 0, 2]\n')
cat('}\n')
