from ..detect import detect_giveaway

def test_detect_giveaway():
    text = """**CONCOURS** Envie de swinguer ? 💃 @VirginRadiofr
    vous offre votre vinyle dédicacé du dernier album de @parov_stelar
    💿

    Pour PARTICIPER ➡ follow @VirginRadiofr
    + RT ce tweet !"""
 
    assert detect_giveaway(text)