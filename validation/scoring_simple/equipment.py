"""Equipment coefficient checks in an isolated generator; no saved build changes."""
import argparse
import json
from pathlib import Path
import shutil
import runtime
from integration import scenario


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ai-root', required=True, type=Path)
    parser.add_argument('--runtime', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    runtime.ROOT = args.ai_root.resolve()
    if not (runtime.ROOT / 'New_AI/Scoring/Equipment.leek').is_file():
        parser.error('--ai-root must contain New_AI/Scoring/Equipment.leek')
    rt = args.runtime.resolve()
    dest = runtime.bundle(rt, 'equipment-probe')
    shutil.copyfile(Path(__file__).with_name('EquipmentProbe.leek'), dest/'Sonde.leek')
    # Diagnostic fixture only: no ordinary combat needs to be played here.
    (dest/'Idle.leek').write_text('// Adversaire inactif pour les assertions.\n', encoding='utf-8')
    case = scenario(dest, rt)
    case['max_turns'] = 1
    for group in case['entities']:
        for entity in group:
            if entity['name'] != 'probe':
                entity['ai'] = f'test/ai/bundles/{dest.name}/Idle.leek'
    path = rt/'equipment-scenario.json'
    path.write_text(json.dumps(case), encoding='utf-8')
    result = runtime.run(rt, [path], rt/'equipment-result.json')[0]
    checks = [json.loads(s.removeprefix('EQUIPMENT_TEST ')) for s in runtime.messages(result, 'EQUIPMENT_TEST ')]
    costs = [json.loads(s.removeprefix('EQUIPMENT_COST ')) for s in runtime.messages(result, 'EQUIPMENT_COST ')]
    errors = [e for e in runtime.logs(result) if len(e) > 3 and e[1] in (7, 8)]
    aborts = [a for a in result['outcome']['fight']['actions'] if a[0] == 1002]
    for check in checks:
        print(check, flush=True)
    print('costs', costs, 'errors', [str(e)[:300] for e in errors[:10]], 'aborts', aborts)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(dict(bundle=dest.name, checks=checks, costs=costs, errors=errors,
        aborts=aborts, engine_sha256=runtime.digest(rt/'generator.jar'), diagnostic_cores=100),
        ensure_ascii=False, indent=2), encoding='utf-8')
    if len(checks) != 22 or len(costs) != 1 or errors or aborts or any(not c['ok'] for c in checks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
