import simpy

from iot_trabalho.receptor import * # Receptor

def main() -> None:
    print("Hello World")

    env = simpy.Environment()
    N = 5
    waitTime = 5

    r1 = Receptor('r1', env, N, waitTime)



    env.run(until=10)


if __name__ == "__main__":
    main()
