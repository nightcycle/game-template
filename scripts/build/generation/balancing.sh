#!/usr/bin/env bash
echo "updating balance modules"
spreadsheet-to-luau -o out/Shared/Balancing/PropData.luau -page 986679452 -id Id -nospace -sheet 1Ezpj7wFaXQ5ulzzqfBCI_ny_sfNM2Aon1K7n2di-BRo
spreadsheet-to-luau -o out/Shared/Balancing/MaterialData.luau -page 268155101 -id Id -nospace -sheet 1Ezpj7wFaXQ5ulzzqfBCI_ny_sfNM2Aon1K7n2di-BRo
