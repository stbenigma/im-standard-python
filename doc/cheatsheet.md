

Remove a bunch of tags:
```
git tag | grep "pattern" | xargs -I %% git push origin ':refs/tags/%%'
```