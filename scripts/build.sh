# update assets
asphalt update -build -verbose -efficient -force #-efficient 

# generate scripts
midas build
datatree build
pseudo-enum build
boot build
style-guide build out/Client/StyleGuide.luau

# build balance directory
spreadsheet-to-luau -o out/Shared/Balancing/Vehicle.luau -page 0  -id Id -nospace -sheet 1-oZ16B2k9k-jj3APokzYILdPj1oavLxmv3CMUQ9Zkr0
spreadsheet-to-luau -o out/Shared/Balancing/City.luau -page 452549796 -id Id -nospace -sheet 1-oZ16B2k9k-jj3APokzYILdPj1oavLxmv3CMUQ9Zkr0
spreadsheet-to-luau -o out/Shared/Balancing/Infrastructure.luau -page 1007097471 -id Id -nospace -sheet 1-oZ16B2k9k-jj3APokzYILdPj1oavLxmv3CMUQ9Zkr0
spreadsheet-to-luau -o out/Shared/Balancing/Merchandise.luau -page 1185151410 -id Id -nospace -sheet 1-oZ16B2k9k-jj3APokzYILdPj1oavLxmv3CMUQ9Zkr0
spreadsheet-to-luau -o out/Shared/Balancing/Loan.luau -page 1673384457 -id Id -nospace -sheet 1-oZ16B2k9k-jj3APokzYILdPj1oavLxmv3CMUQ9Zkr0

# update wally
wally-update major
wally install
rojo sourcemap default.project.json --output sourcemap.json
wally-package-types --sourcemap sourcemap.json Packages

# build scene
scene scene/main default.project.json out/Shared/Scene.luau

# generate final sourcemap
rojo sourcemap default.project.json --output sourcemap.json