# Housekeeping

## Tags

Remove a bunch of tags by grep pattern:

```
git tag | grep "pattern" | xargs -I %% git push origin ':refs/tags/%%'
```

Enable pruning on fetch

```
git config fetch.prune true
git config fetch.pruneTags true
```

Prune tags once:
`git fetch origin --prune-tags`

[Source](https://stackoverflow.com/questions/10491146/in-git-how-do-i-sync-my-tags-against-a-remote-server?lq=1)

# GitHub Actions

[Cleanup GitHub Action runs](https://qmacro.org/autodidactics/2021/03/26/mass-deletion-of-github-actions-workflow-runs/)