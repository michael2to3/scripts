#!/usr/bin/env fish
set org "$argv[1]"

if [ -z "$org" ];
    echo "Give me organization name. Like: ./github-clone.fish google"
    exit 1
end

set temp_dir (mktemp -d)

function fetch_commit_authors;
    set repo $argv[1]
    gh api repos/$org/$repo/commits --paginate --jq '.[].author.login' > $temp_dir/$repo-commit-authors.txt
end

set repos (gh repo list $org --limit 100 --json name --jq '.[].name')

for repo in $repos;
    fetch_commit_authors $repo
end

cat $temp_dir/*.txt | sort -u | grep -v '^\s*$' > $temp_dir/commit-authors.txt

for user in (cat $temp_dir/commit-authors.txt | sort -u | grep -v '^\s*$')
    set user_repos (gh repo list $user --limit 100 --json name,sshUrl --jq '.[] | "\(.sshUrl) \(.name)"')
    for repo in $user_repos
        set ssh_url (echo $repo | awk '{print $1}')
        set repo_name (echo $repo | awk '{print $2}')
        set clone_dir "$user"_"$repo_name"
        gh repo clone $ssh_url $clone_dir
    end
end

rm -rf $temp_dir
