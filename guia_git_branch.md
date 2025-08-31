# Guia Git Branch

## Criar e trocar de branches
- Criar nova branch:
  ```bash
  git branch nome-da-branch
  ```
- Criar e já mudar para ela:
  ```bash
  git checkout -b nome-da-branch
  ```
- Alternativa moderna:
  ```bash
  git switch -c nome-da-branch   # cria e troca
  git switch nome-da-branch      # apenas troca
  ```
- Ver todas as branches:
  ```bash
  git branch
  git branch -a   # inclui remotas
  ```

## Fazer merge
1. Vá para a branch que receberá as alterações (exemplo: `main`):
   ```bash
   git checkout main
   ```
2. Faça o merge da branch desejada:
   ```bash
   git merge feature-x
   ```

- Sempre o merge é feito **a partir da branch que vai receber**.
- Pode mesclar diretamente na `main` sem precisar passar por uma branch intermediária.

## Histórico e commits
- Ver histórico:
  ```bash
  git log
  git log --oneline
  ```
- Ver log de outra branch:
  ```bash
  git log nome-da-branch
  ```

## Navegar no histórico
- Entrar em um commit específico (sem alterar branches):
  ```bash
  git checkout <hash>
  ```
- Voltar para uma branch depois de navegar:
  ```bash
  git checkout main
  ```

## Reverter ou resetar
- Resetar branch atual para um commit (muda a branch!):
  ```bash
  git reset --hard <hash>
  ```
- Reverter alterações criando novo commit:
  ```bash
  git revert <hash>
  ```

## Desfazer merge incorreto
- Se ainda não foi feito *push*:
  ```bash
  git checkout main
  git reset --hard <hash_antes_do_merge>
  ```
- Se já foi feito *push*:
  ```bash
  git checkout main
  git revert -m 1 <hash_do_commit_merge>
  ```

## Corrigir ou descartar branch incorreta
- Resetar branch para commit correto:
  ```bash
  git checkout feature-x
  git reset --hard <hash_estavel>
  ```
- Excluir branch remota:
  ```bash
  git push origin --delete nome-da-branch
  ```

## Sobrescrever histórico no GitHub
- Reescrever branch remota após correção local:
  ```bash
  git checkout main
  git reset --hard <hash_correto>
  git push origin main --force
  ```

⚠️ `push --force` reescreve o histórico remoto, utilize com cautela.

