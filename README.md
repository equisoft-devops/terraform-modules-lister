# terraform-modules-lister

List all modules in the repository and insert that on the markdown file.

## Example

```yaml
name: Generate terraform docs

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
        token: ${{ secrets.PAT }}
    - name: Terraform modules lister
      uses: equisoft-devops/terraform-modules-lister@v0.1.3
      with:
        find-dir: modules/
        output-file: README.md
    - uses: stefanzweifel/git-auto-commit-action@v4
      with:
        commit_message: "terraform-modules-lister: automated action"
```

This will insert the list of module into the README.md file between label `<!-- BEGIN_TF_MODULES -->` and `<!-- END_TF_MODULES -->`.

## Arguments

| Name        | Default     | Description                                                           |
| ----------- | ----------- | --------------------------------------------------------------------- |
| find-dir    | .           | Relative path to the base directory name where to find modules.       |
| output-file | README.md   | File name to insert the modules list                                  |
| tag-suffix  | MODULES     | Customize the label to search in the output-file. For example, AWS will search for `<!-- BEGIN_TF_AWS -->` and `<!-- END_TF_AWS -->`.|
