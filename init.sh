echo "Deploying Lambda λ"
tmux new-session -d -s lambda 'python3 lambda/app.py'
tmux new-session -d -s discordo 'python3 discordo/app.py'
tmux new-session -d -s telegram 'python3 telegram/app.py'