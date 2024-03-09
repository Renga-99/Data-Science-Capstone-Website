# Python Snake Game

This is a snake game in python. The default characters are as below.

- Snake: `#`
- Food: `*`
- Background: `.`

## How to play

WASD or arrow keys for snake movement. Q to quit. Any other key to pause. Press one of the movement keys to resume.

## Running the game

```bash
python3 snake.py [flags]
```

### Flags

See `snake.py --help`

### Example configurations

```bash
python3 snake.py --char-head='☺' --char-snake='+' --char-bg=' '
python3 snake.py --color-snake blue --color-food red
```

## Todo

- [X] Make horizontal and vertical speeds equal
- [ ] Fix pausing (save state and unpause at same state)
