from hypothesis import given, strategies as st
from models.claim_schema import ReclamacionInsurance, ItemReclamado
from services.xml_parser import XMLClaimParser
from services.claim_transformer import ClaimTransformerService


st_item = st.builds(
    ItemReclamado,
    item_id=st.text(min_size=1, max_size=10),
    descripcion=st.text(min_size=3, max_size=30),
    monto_estimado=st.floats(min_value=1.0, max_value=10000.0),
    categoria=st.sampled_from(["vehicular", "hogar", "salud"])
)


@given(
    claim_id=st.text(min_size=3, max_size=10),
    poliza_num=st.text(min_size=10, max_size=10).map(lambda s: f"POL-{s}"),
    cliente_id=st.text(min_size=3, max_size=10),
    monto=st.floats(min_value=0.0, max_value=100000.0),
    descripcion=st.text(min_size=5, max_size=100),
    items=st.lists(st_item, min_size=1, max_size=5)
)
def test_xml_generation_and_parsing_property(
    claim_id, poliza_num, cliente_id, monto, descripcion, items
):
    items_xml = "".join([
        f"""
        <item>
            <item_id>{i.item_id}</item_id>
            <descripcion>{i.descripcion}</descripcion>
            <monto_estimado>{i.monto_estimado}</monto_estimado>
            <categoria>{i.categoria}</categoria>
        </item>
        """
        for i in items
    ])

    xml_str = f"""
    <reclamacion>
        <id_reclamacion>{claim_id}</id_reclamacion>
        <numero_poliza>{poliza_num}</numero_poliza>
        <id_cliente>{cliente_id}</id_cliente>
        <fecha_incidente>2026-10-27</fecha_incidente>
        <tipo_siniestro>Accidente</tipo_siniestro>
        <monto_total_reclamado>{monto}</monto_total_reclamado>
        <descripcion_hechos>{descripcion}</descripcion_hechos>
        <items>{items_xml}</items>
    </reclamacion>
    """

    result_json = ClaimTransformerService.process_xml_to_ai_json(xml_str)

    assert "metadata" in result_json
    assert "canonical_text_for_embedding" in result_json
    assert result_json["metadata"]["id_reclamacion"] == claim_id
    assert result_json["metadata"]["id_cliente"] == cliente_id