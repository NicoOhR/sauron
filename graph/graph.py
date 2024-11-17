import random
import os

# size of nxn square matrix
n = 10

matrix = [
    ["1" if (random.choice([True, False]) and i > j) else "0" for i in range(n)]
    for j in range(n)
]

with open("graph", "w") as file:
    file.write("\n".join([" ".join(row) for row in matrix]))

orcs = [
    "gazgash",
    "gazbug",
    "gazhorn",
    "gazmog",
    "gazmuz",
    "gazrad",
    "gazrat",
    "gazthak",
    "gazlag",
    "gazluk",
    "gazlun",
    "gazlur",
    "gaznag",
    "gazuf",
    "gazug",
    "gazul",
    "ghash",
    "golfimbul",
    "gorbag",
    "gorbug",
    "gorduf",
    "gordush",
    "gorgash",
    "gorgaz",
    "gorhur",
    "gorluk",
    "gorlun",
    "gornag",
    "gorshag",
    "gorthak",
    "gorul",
    "gorzag",
    "grishnákh",
    "lagbug",
    "lagduf",
    "lagdush",
    "laghur",
    "laguf",
    "laglug",
    "laglun",
    "lagrad",
    "lagrat",
    "lagthak",
    "lug",
    "lugbag",
    "lugduf",
    "lugdush",
    "lughorn",
    "lughur",
    "lugluk",
    "luglun",
    "lugnag",
    "lugthak",
    "lugul",
    "lugzag",
    "lunbag",
    "lunbug",
    "lunduf",
    "lundush",
    "lungash",
    "lungaz",
    "lungor",
    "lunhur",
    "lunlag",
    "lunluk",
    "lunmaz",
    "lunrad",
    "lunrat",
    "lunshag",
    "lunthak",
    "lunuf",
    "lunug",
    "lunul",
    "lunzag",
    "maubag",
    "maubug",
    "mauduf",
    "maudush",
    "maugash",
    "maugaz",
    "maugor",
    "mauhur",
    "mauluk",
    "maulur",
    "maunag",
    "mauthak",
    "mauzag",
    "muzbag",
    "muzbug",
    "muzduf",
    "muzdush",
    "muzgash",
    "muzgaz",
    "muzgor",
    "muzhur",
    "muzlag",
    "muzlug",
    "muzluk",
    "muzlun",
    "muzlur",
    "muznag",
    "muzrad",
    "muzrat",
    "muzthak",
    "muzug",
    "muzul",
    "nagbug",
    "nagduf",
    "nagdush",
    "naghur",
    "naglug",
    "nagluk",
    "naglur",
    "nagmuz",
    "nagug",
    "nagrad",
    "nagrat",
    "nagthak",
    "nagzag",
    "nuzu",
    "radbag",
    "radbug",
    "radgash",
    "radgaz",
    "radhur",
    "radlag",
    "radluk",
    "radmuz",
    "radnag",
    "radrat",
    "radthak",
    "radug",
    "radzag",
    "shagbug",
    "shagduf",
    "shagdush",
    "shagluk",
    "shaglur",
    "shagrad",
    "shagrat",
    "shagthak",
    "shaguf",
    "shagug",
    "shagul",
    "snaga",
    "ufgaz",
    "uflug",
    "ufluk",
    "ufthak",
    "ufzag",
    "ugbag",
    "ugduf",
    "ugdush",
    "ughur",
    "uglag",
    "ugluk",
    "uglur",
    "ugmuz",
    "ugnag",
    "ugrad",
    "ugrat",
    "ugthak",
    "ugzag",
    "yagaz",
    "yagbug",
    "yagduf",
    "yagdush",
    "yaghur",
    "yaglug",
    "yaglun",
    "yagluk",
    "yagmuz",
    "yagor",
    "yagrad",
    "yagrat",
    "yagthak",
    "yaguf",
    "yagug",
    "yagul",
    "zagbug",
    "zagduf",
    "zagdush",
    "zaghur",
    "zaglag",
    "zaglug",
    "zaglun",
    "zagluk",
    "zagmuz",
    "zagrad",
    "zagrat",
    "zagthak",
    "zaguf",
    "zagug",
]

orcs_out_map = {
    orc: "".join([f',"{orcs[j]}"' for (j, b) in enumerate(matrix[i]) if b == "1"])
    for (i, orc) in enumerate(map(lambda x: orcs[x], range(n)))
}

orcs_in_map = {
    orc: "".join(
        [
            f'"{orcs[k]}",'
            for (k, b) in enumerate([matrix[j][i] for j in range(n)])
            if b == "1"
        ]
    )
    for (i, orc) in enumerate(map(lambda x: orcs[x], range(n)))
}


def kubernetes_file_generation():
    import yaml
    from copy import copy

    with open("../kubernetes/graph-node.yml", "r") as fp:
        data_src = fp.read()

    results = []

    for _, orc in zip(range(n), orcs):
        data = copy(data_src)

        data.replace("\{\{orc\}\}", orc)

        manifest = yaml.safe_load(data)

        # substitute orc name
        manifest["metadata"]["name"] = orc
        manifest["spec"]["selector"]["matchLabels"]["app"] = orc
        # modify args in place
        inputs = []
        for i in range(n):
            if matrix[i][_] == "1":
                inputs.append(orcs[i])

        outputs = []
        for i in range(n):
            if matrix[_][i] == "1":
                outputs.append(orcs[i])

        if inputs:
            inputs = ["-i"] + inputs

        if outputs:
            outputs = ["-o"] + outputs

        args = inputs + outputs
        manifest["spec"]["template"]["spec"]["containers"][0]["args"] = args
        manifest["spec"]["template"]["spec"]["containers"][0]["env"] = [
            {"name": "KAFKA_API_KEY", "value": str(os.getenv("KAFKA_API_KEY"))},
            {"name": "KAFKA_API_SECRET", "value": str(os.getenv("KAFKA_API_SECRET"))},
        ]
        results.append(manifest)

    # print(yaml.dump_all(results, indent=3))
    with open("../kubernetes/graph-node-output.yml", "w+") as fp:
        yaml.dump_all(results, fp)


def terraform_graph_generation():
    with open("../terraform/graph.tf", "w") as file:
        for orc in map(lambda x: orcs[x], range(n)):
            file.write(
                f"""
    resource "{orc}" {{
        topic_name = "{orc}"
        lifecycle {{
            prevent_destroy = true
        }}
    }}
    """
            )


def terraform_kubernetes_generation():
    with open("../terraform/graph.tf", "w") as file:
        for orc in map(lambda x: orcs[x], range(n)):
            file.write(
                f"""
resource "confluent_kafka_topic" "{orc}" {{
    topic_name = "{orc}"
}}
    """
            )

    with open("../terraform/kubernetes.tf", "w") as file:
        file.write(
            """
provider "kubernetes" {
  config_path    = "~/.kube/config"
}
    """
        )
        for orc in map(lambda x: orcs[x], range(n)):
            file.write(
                f"""
resource "kubernetes_deployment" "orc-{orc}" {{
  metadata {{
    name = "orc-{orc}"
  }}
  spec {{
    replicas = 1
    selector {{
      match_labels = {{
        app = "orc-{orc}"
      }}
    }}

    template {{
      metadata {{
        labels = {{
          app = "orc-{orc}"
        }}
      }}

      spec {{
        container {{
          name = "orc-{orc}"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , {orcs_in_map[orc]} "-o" {orcs_out_map[orc]} ]
          command = [ "python3", "main.py" ]
          env {{
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }}
          env {{
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }}
        }}
      }}
    }}
  }}
}}
    """
            )


if __name__ == "__main__":
    # kubernetes_file_generation()
    terraform_graph_generation()
    terraform_kubernetes_generation()
