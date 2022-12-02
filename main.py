from experiment import *

print ('Enter "test" instead of PID to run plot test.')
while True:
  pid = input("Enter PID: ")

  if pid.isnumeric():
    print()
    run_experiment(pid)
    break
  elif pid.lower() == 'test':
    plot_test()
    break
  else:
    print('Invalid input!')

print('###################')
print('### PROGRAM END ###')
print('###################')