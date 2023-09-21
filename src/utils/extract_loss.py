
def extract_numbers_from_file(filename, output_filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    results = []

    for line in lines[88:]:
        if line.startswith("[Sep"):  # Assuming date always starts with [Sep
            loss = line[line.find(']') + 1:].strip().split()
            if loss[0].isdigit():
                results.append(loss)

    with open(output_filename, 'w') as file:
        for result in results:
            file.write(' '.join(result) + '\n')


if __name__ == "__main__":
    filename = "/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/MSMARCO_TRAINING_256.out"
    output_filename = "training_loss_256.txt"
    print(extract_numbers_from_file(filename, output_filename))