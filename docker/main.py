import sys, json

from function import main

if __name__ == "__main__":
    import sys, json
    maybe_event = json.loads(sys.argv[1])
    if isinstance(maybe_event, list):
        for event in maybe_event:
            print(main(event))
    else:
        print(main(maybe_event))
