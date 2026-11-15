import json
from services.claim_transformer import ClaimTransformerService


def main():
    with open("data/sample_claim.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    result = ClaimTransformerService.process_xml_to_ai_json(xml_content)

    print("\n========== RESULTADO JSON ==========\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()