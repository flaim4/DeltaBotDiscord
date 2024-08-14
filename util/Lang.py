
class Lang:
    def __init__(self):
        self.data = {}

    def load(self, reader):
        try:
            end = True
            commit = False
            prefix = ""

            for line in reader:
                line = line.strip()
                
                if line.startswith("<"):
                    if ">" not in line:
                        commit = True
                elif commit:
                    if ">" in line:
                        commit = False
                elif line.startswith("#{") and line.endswith("}"):
                    prefix = line[2:-1]
                    end = False
                elif line.startswith("#end"):
                    end = True
                elif line.startswith("//"):
                    continue
                elif "=" in line:
                    parts = line.split("=", 1)
                    key = parts[0].strip()
                    if not end:
                        key = prefix + key
                    self.put(key, parts[1].strip())
        except IOError as e:
            print(e)

        return self

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data[key]

    def __repr__(self):
        return f"{self.data}"