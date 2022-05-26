import os

def find_files(filename, search_path):
   result = []

   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result[0]


def main():
    composeFilePath = find_files("docker-compose.yml","/home/ubuntu/Tools/ClientScans")
    dir = os.path.dirname(composeFilePath)
    os.chdir(dir)
    os.system("docker compose up -d")
main()