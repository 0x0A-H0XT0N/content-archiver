import tty
import sys
import termios

print("press any key to continue")

original_stdin_settings = termios.tcgetattr(sys.stdin)    # get the original setting for the "stdin" and puts it on a variable to
# be called later and be restored

tty.setcbreak(sys.stdin)    # set "stdin" in raw mode
user_input = None
while user_input is None:   # enquanto nenhuma tecla eh apertada
    user_input = sys.stdin.read(1)[0]    # leia a entrada "stdin" que esta em raw mode e
    # armazene como entrada de usuario
    print("current attr:", termios.tcgetattr(sys.stdin))
    print("original attr:", original_stdin_settings)
    print("key press detected")

# while x != chr(27):     # ESC
#     x = sys.stdin.read(1)[0]
#     print("You pressed", x)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_stdin_settings)
