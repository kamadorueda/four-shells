# Standard library
import argparse
import os
import json


DATA = os.environ['DATA']


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rev-data', required=True)
    parser.add_argument('--rev-sha', required=True)
    parser.add_argument('--rev-summary', required=True)
    parser.add_argument('--rev-timestamp', required=True)
    parser.add_argument('--revs', required=True)

    return parser.parse_args()


def json_load(path: str, default = None):
    try:
        with open(path) as handle:
            return json.load(handle)
    except FileNotFoundError:
        if default is None:
            raise
        return default


def json_dump(path: str, data) -> None:
    with open(path, 'w') as handle:
        json.dump(data, handle, indent=1, sort_keys=True)


def load_revs(path):
    with open(path) as handle:
        revs = handle.read().splitlines()

    data = {}
    index = 0
    for index, sha in enumerate(revs):
        data[sha] = index
    data[None] = index + 1

    return data


def main() -> None:
    args = cli()

    print(f'processing: {args.rev_sha}')

    revs2index = load_revs(args.revs)
    revs = list(revs2index.keys())

    for pkg, meta in json_load(args.rev_data).items():
        version = meta['version']
        if not version:
            continue

        meta = {
            'description': meta['meta'].get('description', ''),
            'homepage': meta['meta'].get('homepage', ''),
            'license': meta['meta'].get('license', None),
            'long_description': meta['meta'].get('longDescription', ''),
            'maintainers': meta['meta'].get('maintainers', []),
            'name': meta['pname'],
            'position': os.path.relpath(meta['meta'].get('position', 'nixpkgs/'))[8:],
            'platforms': meta['meta'].get('platforms', None),
        }

        data = json_load(f'{DATA}/pkgs/{pkg}.json', {})

        if version not in data:
            data[version] = {
                'meta': meta,
                'revs': [args.rev_sha, args.rev_sha],
            }
            json_dump(f'{DATA}/badges/{pkg}.json', {
                'label': '',
                'message': f'{len(data)} releases',
                'schemaVersion': 1,
            })
            json_dump(f'{DATA}/pkgs/{pkg}.json', data)
        elif (
            data[version]['revs'][1] not in revs2index
            or revs2index[args.rev_sha] < revs2index[data[version]['revs'][1]]
        ):
            data[version]['revs'][1] = args.rev_sha
            json_dump(f'{DATA}/pkgs/{pkg}.json', data)
        elif (
            data[version]['revs'][0] not in revs2index
            or revs2index[args.rev_sha] > revs2index[data[version]['revs'][0]]
        ):
            data[version]['revs'][0] = args.rev_sha

    # Update global references
    json_dump(f'{DATA}/pkgs.json', [
        pkg[0:-5] for pkg in sorted(os.listdir(f'{DATA}/pkgs'))
    ])
    json_dump(f'{DATA}/revs.json', revs[0:-1])

    # Append the current revision
    json_dump(f'{DATA}/revs/{args.rev_sha}.json', {
        'summary': args.rev_summary,
        'timestamp': args.rev_timestamp,
    })


if __name__ == '__main__':
    main()
