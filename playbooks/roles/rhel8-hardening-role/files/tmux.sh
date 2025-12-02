if [ "$PS1" ]; then
  parent=$(ps -o ppid= -p $$)
  name=$(ps -o comm= -p $parent)
  # For convenience changed "tmux" to "tmux attach || tmux"
  # This will automatically attach your previous tmux session or create a new one if a session doesn't exist
  case "$name" in (sshd|login) tmux attach || tmux ;; esac
fi