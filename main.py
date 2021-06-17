from docxtpl import DocxTemplate
import math

doc = DocxTemplate("Memoria de cálculos del estribo cim superficial.docx")

def design(params):
    # params: parámetros del diseño
    # fc_estribo: resistencia del concreto estribo, MPa
    # fc_supeestructura: resistencia del concreto de la superestructura, MPa
    # E_acero: Módulo de elasticidad del acero, MPa
    # numero_carriles: número de carriles en el puente


    #Datos de entrada
    fc_estribo = params['fc_estribo'] = params.get('fc_estribo', 21)

    fc_superestructura = params['fc_superestructura'] = params.get('fc_superestructura', 28)
    
    E_acero = params['E_acero'] = params.get('E_acero', 200000)

    fy = params['fy'] = params.get('fy', 420)

    numero_carriles = params['numero_carriles'] = params.get('numero_carriles', 1)

    #Materiales

    # pesoespecifico_concreto: Peso especifico del concreto, kN/m3
    # pesoespecifico_carpetaasfaltica: Peso especifico de la carpeta asfaltica, kN/m3

    pesoespecifico_concreto = params['pesoespecifico_concreto'] = params.get('pesoespecifico_concreto', 23.544)

    pesoespecifico_carpetaasfaltica = params['pesoespecifico_carpetaasfaltica'] = params.get('pesoespecifico_carpetaasfaltica', 21.582)

    ## Información estudio de suelos
    # tipodesuelo: tipo de suelo definidos en CCP-14, Figuras 11.6.3.2-1 y 11.6.3.2-2
    # pesoespecifico_suelo: peso específico del suelo, kN/m3
    # capacidaddecarganominaldelsuelo: capacidad de carga nominal del suelo, MPa, Art. 10.6.3
    # angulodefriccioninternadelsuelodecimentacion: ángulo de friccion interna del suelo de cimentacion, °
    # perfildelsuelo: Perfil del suelo, Tabla 3.10.3.1
    
    tipodesuelo = params['tipodesuelo'] = 'no rocoso'

    pesoespecifico_suelo = params['pesoespecifico_suelo'] = params.get('pesoespecifico_suelo', 19.61) 

    capacidaddecarganominaldelsuelo = params['capacidaddecarganominaldelsuelo'] = params.get('capacidaddecarganominaldelsuelo', 1)

    angulodefriccioninternadelsuelodecimentacion = params['angulodefriccioninternadelsuelodecimentacion'] = params.get('angulodefriccioninternadelsuelodecimentacion', 30)

    perfildelsuelo = params['perfildelsuelo'] = 'Perfil C'

    ## Estados limite 

    #Estado limite de resistencia
    # factorderesistencia: Factor de resistencia de estado límite de resistencia, Art. 10.5.5.2
    # factorderesistencia_servicio: Factor de resistencia de estado límite de servicio, Art. 11.5.7 y Art. 11.6.2.3
    # factorderesistencia_eventoextremo: Factor de resistencia de estado límite de evento extremo , Art. 11.5.8 y Art. C11.6.1.1-1
    #
    # capacidadportantemayoradadelsuelo: capacidad portante mayorada del suelo para el estado límite de resistencia I, kN/m2, Art. 10.6.3.1.1-1
    # capacidadportantemayoradadelsuelo_servicio: capacidad portante mayorada del suelo para el estado límite de servicio, kN/m2, Art. 10.6.3.1.1-1
    # capacidadportantemayoradadelsuelo_eventoextremo: capacidad portante mayorada del suelo para el estado límite de evento extremo, kN/m2, Art. 10.6.3.1.1-1
    
    factorderesistencia = params['factorderesistencia'] = params.get('factorderesistencia', 0.45)

    capacidadportantemayoradadelsuelo = params['capacidadportantemayoradadelsuelo'] = factorderesistencia * capacidaddecarganominaldelsuelo

    factorderesistencia_servicio = params['factorderesistencia_servicio'] = params.get('factorderesistencia_servicio', 0.65 )

    capacidadportantemayoradadelsuelo_servicio = params['capacidadportantemayoradadelsuelo_servicio'] = factorderesistencia_servicio * capacidaddecarganominaldelsuelo

    factorderesistencia_eventoextremo = params['factorderesistencia_eventoextremo'] = params.get('factorderesistencia_eventoextremo', 0.8)

    capacidadportantemayoradadelsuelo_eventoextremo = params['capacidadportantemayoradadelsuelo_eventoextremo'] = factorderesistencia_eventoextremo * capacidaddecarganominaldelsuelo 

    ## Clasificación sismica del puente
    # municipio: Municipio donde se localiza el proyecto
    # departamento: Departamento al cual pertenece el municipio
    # PGA: coeficiente de acelearación pico del terreno, Figura 3.10.2.1-1
    # S1: coeficiente de eaceleración espesctral horizontal, periodo 1s, Figura 3.10.2.1-3
    # clasificacionoperacional: Clasificación operacional, Art. 3.10.5
    # factordesitio: Factor de sitio,  Tabla 3.10.3.2-3
    #
    # zonadedesempeño sísmico: Zona de desempeño sísmico, Tabla 3.10.6-1

    municipio = params['municipio'] = 'Armenia'
    
    departamento = params['departamento'] = 'Quindio'

    PGA = params['PGA'] =params.get('PGA', 0.35)

    S1 = params['S1'] = params.get('S1', 0.3)

    clasificacionoperacional = params['clasificacionoperacional'] = 'Otros puentes'

    factordesitio = params['factordesitio'] = params.get('factordesitio', 1.5)

    SD1 = params['SD1'] = round(factordesitio * S1, 2)

    if SD1 < 0.15 :
        zonadedesempeñosismico = 'Zona 1'
    elif SD1 > 0.15 and SD1 < 0.3 :
        zonadedesempeñosismico = 'Zona 2'
    elif SD1 > 0.3 and SD1 < 0.5 :
        zonadedesempeñosismico = 'Zona 3'
    else :
        zonadedesempeñosismico = 'Zona 4'
    
    params['zonadedesempeñosismico'] = zonadedesempeñosismico

    #Dimensiones del estribo
    # altura_estribo: Altura del estribo, m
    # ancho_estribo: Ancho del estribo, m
    # largo_estribo: Largo del estribo, m
    # altura_vastago: Altura del vástago, m
    # espesor_vástago: Espesor del vástago, m
    # altura_base: Altura de la base del estribo, m
    # ancho_base: Ancho de la base del estribo, m
    # altura_talon: Altura del talón, m
    # ancho_talon: Ancho del talón, m
    # altura_espaldar: Altura del espaldar, m
    # espesor_espaldar: Espesor del espaldar, m
    # distanciaalabase_espaldar: distancia desde el espaldar a la base del estribo, m
    # cantidad_topes: Cantidad de topes sísmicos, m
    # altura_topes: Altura de los topes sísmicos, m
    # largo_topes: Largo de los topes sísmicos, m
    # ancho_topes: Ancho de los topes sísmicos, m
    # cantidad_aletas: Cantidad de las aletas, m
    # altura_aletas: Altura de las aletas, m
    # espesor_base_aletas: Espesor de la base de las aletas, m
    # espesor_corona_aletas: Espesor de la corono de las aletas, m
    #  
    #Estribo
    #  
    altura_estribo = params['altura_estribo'] = params.get('altura_estribo', 3) 

    ancho_estribo = params['ancho_estribo'] = params.get('ancho_estribo', 2.6)

    largo_estribo = params['largo_estribo'] = params.get('largo_estribo', 3) 

    #Vastago
    altura_vastago = params['altura_vastago'] = params.get('altura_vastago', 1.15)
    espesor_vastago = params['espesor_vastago'] = params.get('espesor_vastago', 0.5)

    #Base
    altura_base = params['altura_base'] = params.get('altura_base', 0.5)
    ancho_base = params['ancho_base'] = params.get('ancho_base', 1.5)

    #Talon
    altura_talon = params['altura_talon'] = params.get('altura_talon', 0.5)
    ancho_talon = params['ancho_talon'] = params.get('ancho_talon', 1.1)

    #Espaldar
    altura_espaldar = params['altura_espaldar'] = params.get('altura_espaldar', 1.35)
    espesor_espaldar = params['espesor_espaldar'] = params.get('espesor_espaldar', 0.25)
    distanciaalabase_espaldar = params['distanciaalabase_espaldar'] = params.get('distanciaalabase_espaldar', 1.35)

    #Topes sismicos
    cantidad_topes = params['cantidad_topes'] = params.get('cantidad_topes', 2)
    altura_topes = params['altura_topes'] = params.get('altura_topes', 0.6) 
    largo_topes = params['largo_topes'] = params.get('largo_topes', 0.3)
    ancho_topes = params['ancho_topes'] = params.get('ancho_topes', 0.45)

    #Aletas

    cantidad_aletas = params['cantidad_aletas'] =params.get('cantidad_aletas', 2)
    altura_aletas = params['altura_aletas'] = params.get('altura_aletas', 2.5)
    ancho_aletas = params['ancho_aletas'] = params.get('ancho_aletas', 1.2)
    espesor_base_aletas = params['espesor_base_aletas'] = params.get('espesor_base_aletas', 0.25)
    espesor_corona_aletas = params['espesor_corona_aletas'] = params.get('espesor_corona_aletas', 0.25)

    ##Superestructura
    # peso_losa: peso de la losa por m de largo, m2
    # L_superestructura:  Longitud de la superestructura, m
    # cantidad_vigas: Cantidad de vigas
    # peso_vigas: peso de las vigas por m de largo, m
    # peso_anden: peso del área transversal del anden por m de largo, m2
    # peso_bordillo:peso del bordillo por m de largo, m2
    # peso_barandas: peso de las barandas del puente, kN/m
    # ancho_carpetaasfaltica: Ancho de la carpeta asfáltica, m
    # espesor_carpetaasfaltica: Espesor de la carpeta asfáltica, m
    #  
    # Losa
    peso_losa = params['peso_losa'] = params.get('peso_losa', 0.522)

    L_superestructura = params['L_superestructura'] = params.get('L_superestructura', 28)

    #Vigas
    cantidad_vigas = params['cantidad_vigas'] = params.get('cantidad_vigas', 3)
    peso_vigas = params['peso_vigas'] = params.get('peso_vigas', 1.3)

    #Anden
    peso_anden = params['peso_anden'] = params.get('peso_anden', 0.25)

    #Bordillo
    peso_bordillo = params['peso_bordillo'] = params.get('peso_bordillo', 0.07 )
   
    #Barandas
    peso_barandas = params['peso_barandas'] = params.get('peso_barandas', 1.5) 

    #Carpeta asfaltica
    ancho_carpetaasfaltica = params['ancho_carpetaasfaltica'] = params.get('ancho_carpetaasfaltica', 6) 

    espesor_carpetaasfaltica = params['espesor_carpetaasfaltica'] = params.get('espesor_carpetaasfaltica', 0.1) 

    #Cargas y momentos provenientes de la superestructura
    # DC_losa: Carga permanente debido al peso propio de la losa sobre el estribo, kN
    # DC_vigas; Carga permanente debido al peso propio de las vigas sobre el estribo, kN
    # DC_sobreimpuestas: Cargas sobre el estribo debido al peso del bordillo, anden, y barandas, kN
    # DW: Carga sobre el estribo debido al peso de la carpeta asfáltica, kN
    #
    # DW_m: Carga sobre el estribo debido al peso de la carpeta asfáltica por m de ancho de estribo, kN
    # DC_total_supestructura: Cargas permanentes provenientes de la superestructura, kN
    # DC_total_superestructura_m:  Cargas permanentes provenientes de la superestructura por m de ancho de estribo, kN
    # X_a: Distancia de aplicación de DC_total_superestructura_m con respecto al punto A, m
    # M_a_DC: Momento de estabilización con respecto al punto A debido a DC_total_superestructura_m, kNm/m
    # M_a_DW: Momento de estabilización con respecto al punto A debido a DW_m, kNm/m


    DC_losa = params['DC_losa'] = round(peso_losa * L_superestructura/2, 2)

    DC_vigas = params['DC_vigas'] = round(cantidad_vigas * peso_vigas* L_superestructura/2, 2)

    DC_sobreimpuestas = params['DC_sobreimpuestas'] = round((peso_anden + peso_bordillo) * L_superestructura/2 + peso_barandas * L_superestructura/2, 2)

    DW = params['DW'] = round(ancho_carpetaasfaltica * espesor_carpetaasfaltica * pesoespecifico_carpetaasfaltica * L_superestructura/2, 2)
    
    DW_m = params['DW_m']= round(DW / largo_estribo, 2)

    #Resumen de cargas y momentos provenientes de superestructura por ancho
    #Momento de estabilizacion debido a las cargas permanentes provenientes de la superestructura
    DC_total_superestructura = params['DC_total_superestructura'] = DC_losa + DC_sobreimpuestas + DC_vigas 
    DC_total_superestructura_m = params['DC_total_superestructura_m'] = round(DC_total_superestructura / largo_estribo, 2)
    
    X_a = params['X_a'] = round(ancho_base - (espesor_vastago / 2), 2)
    M_a_DC = params['M_a_DC'] = round(DC_total_superestructura / largo_estribo * X_a, 2) 
    M_a_DW = params['M_a_DW'] = round(DW / largo_estribo * X_a, 2 )

    #Cargas provenientes de la superestructura debidas a la carga vehicular de diseño
    # carga_primereje_camion: Carga sobre el primer eje del camión de diseño CCP-14, kN
    # carga_segundoeje_camion: Carga sobre el segundo eje del camión de diseño CCP-14, kN
    # carga_tercereje_camion: Carga sobre el tercer eje del camión de diseño CCP-14, kN
    # carga_total_camion: Carga total del camión de diseño CCP 14, kN
    # distancia_ejes1y2_camión: Distancia entre el primer eje y el segundo eje del camión, m
    # distancia_ejes2y3_camión: Distancia entre el segundo eje y el tercer eje del camión, m
    # carga_primereje_tandem: Carga sobre el primer eje del tándem de diseño CCP-14, kN
    # carga_segundoeje_tandem: Carga sobre el segundo eje del tándem de diseño CCP-14, kN
    # distancia_ejes1y2_tandem: Distancia entre el primer eje y el segundo eje del tándem, m
    # carga_total_tándem: Carga total del tándem de diseño CCP 14, kN
    # carga_carrildiseño: Carga debida al carril de diseño CCP-14, kN/m

    # carga_camion_estribo: Carga producida por el camión de diseño sobre el estribo, kN
    # carga_tandem_estribo: Carga producida por el tándem de diseño sobre el estribo, kN
    # carga_carrildiseño_estribo: Carga producida por el carril de diseño sobre el estribo, kN
    # factor_cargadinamica: Factor de carga dinámica 
    # factor_presencia_multiple: Factor de presencia multiple para dos carriles cargados
    # carga_vehicular_uncarril: Carga sobre el estribo debida a la carga vehicular de diseño CCP-14 para un carril cargado, kN
    # carga_vehicular_doscarriles: Carga sobre el estribo debida a la carga vehicular de diseño CCP-14 para dos carriles cargados, kN
    # carga_vehicular_por_m_ancho_estribo: Carga por m de ancho de estribo debido a la carga vehicular de diseño CCP-14, kN/m
    # M_a_LLIM: Momento de estabilización con respecto al punto A debido a la carga vehicular de diseño, kNm/m
     
    # Carga Camión de diseño

    carga_primereje_camion = params['carga_primereje_camion']= 160
    carga_segundoeje_camion = params['carga_segundoeje_camion']= 160
    carga_tercereje_camion = params['carga_tercereje_camion'] = 40
    carga_total_camion = params['carga_total_camion']= carga_primereje_camion + carga_segundoeje_camion + carga_tercereje_camion
    distancia_ejes1y2_camion = params['distancia_ejes1y2_camion'] = 4.3 
    distancia_ejes2y3_camion = params['distancia_ejes2y3_camion'] = 4.3

    #Tandem de diseño
    carga_primereje_tandem = params['carga_primereje_tandem']= 125 
    carga_segundoeje_tandem = params['carga_segundoeje_tandem']= 125
    distancia_ejes1y2_tandem = params['distancia_ejes1y2_camion'] = 1.2
    cargatotal_tandem = params['cargatotal_tandem']= carga_primereje_tandem + carga_segundoeje_tandem

    #Carril de diseño
    carga_carrildiseño = params['carga_carrildiseño'] = 10.3

    carga_camion_estribo = params['carga_camión_estribo']= carga_primereje_camion * 1 + carga_segundoeje_camion * (1 - distancia_ejes1y2_camion / L_superestructura) + carga_tercereje_camion * (1 - (distancia_ejes1y2_camion + distancia_ejes2y3_camion)/L_superestructura )
    carga_tandem_estribo = params['carga_tandem_estribo']= carga_primereje_tandem * 1 + carga_segundoeje_tandem * (1 - distancia_ejes1y2_tandem / L_superestructura)
    carga_carrildiseño_estribo = params['carga_carrildiseño_estribo'] = carga_carrildiseño * L_superestructura / 2 * 1

    #Carga sobre el estribo dibido a la carga vehicular de diseño
    factor_cargadinamica = params['factor_cargadinamica'] = 1.33

    factor_presenciamultiple = params['factor_presenciamultiple'] = 1

    if carga_camion_estribo > carga_tandem_estribo :
        carga_vehicular_uncarril = round(factor_cargadinamica * carga_camion_estribo + carga_carrildiseño_estribo, 2)
    else :
        carga_vehicular_uncarril = round(factor_cargadinamica * carga_tandem_estribo + carga_carrildiseño_estribo, 2)

    params['carga_vehicular_uncarril'] = carga_vehicular_uncarril 

    carga_vehicular_doscarriles = params['carga_vehicular_doscarriles'] = round(numero_carriles * carga_vehicular_uncarril, 2) 

    carga_vehicular_por_m_ancho_estribo = params['carga_vehicular_por_m_ancho_estribo'] = round(carga_vehicular_doscarriles / largo_estribo, 2)

    #Momento de estabilización con respecto al punto A debido a la carga vehicular de diseño
    M_a_LLIM = params['M_a_LLIM'] = round(carga_vehicular_por_m_ancho_estribo * X_a, 2)

    #Fuerza de Frenado
    # BR_25: 25% del peso de los ejes del camión o tándem de diseño, kN
    # BR_5: 5% del camión o tándem de diseño más la carga de carril, kN
    # BR_m_ancho: Fuerza de frenado por m de ancho de estribo, kN/m
    # M_a_BR: Momento de desestabilización con respecto al punto A debido a la fuerza de frenado, kNm/m
     
    BR_25 = params['BR_25'] = numero_carriles * factor_presenciamultiple * 0.25 * carga_total_camion
    BR_5 = params['BR_5'] = 0.05 *numero_carriles * factor_presenciamultiple * (carga_total_camion + carga_carrildiseño * L_superestructura/2) 
    if BR_25 > BR_5 :
        BR_m_ancho = BR_25 / largo_estribo
    else :
        BR_m_ancho = BR_5 / largo_estribo

    params['BR_m_ancho'] = BR_m_ancho
    M_a_BR = params['M_a_BR'] = BR_m_ancho * (altura_estribo + 1.8 )

    #Cargas y momentos debidos al peso de la subestructura
    # DC_'parte de estribo': Peso del concreto de la 'parte de estribo' por m de ancho de estribo, kN/m
    # X_a_'parte de estribo': Distancia en el eje x desde el punto A hasta el centro de gravedad de la 'parte de estribo', m 
    # Y_a_'parte de estribo': Distancia en el eje y desde el punto A hasta el centro de gravedad de la 'parte de estribo', m
    # DC_X_a_'parte de estribo': Momento generado por peso de la 'parte de estribo' sobre el Punto A, kNm/m
    # DC_Y_a_'parte de estribo': Momento generado por peso de la 'parte de estribo' sobre el Punto A, kNm/m

    

    #Peso del estribo
    DC_zapata = pesoespecifico_concreto *(ancho_base + ancho_talon) * ((altura_base + altura_talon) / 2)
    X_a_zapata = (ancho_base +ancho_talon) / 2
    Y_a_zapata = ((altura_base + altura_talon) / 2) / 2
    DC_X_a_zapata = DC_zapata * X_a_zapata
    DC_Y_a_zapata = DC_zapata * Y_a_zapata
    
    params['DC_zapata'] = round(DC_zapata, 2)
    params['X_a_zapata'] = round(X_a_zapata, 3)
    params['Y_a_zapata'] = round(Y_a_zapata, 3)
    params['DC_X_a_zapata'] = round(DC_X_a_zapata, 2)
    params['DC_Y_a_zapata'] = round(DC_Y_a_zapata,2)

    DC_vastago = pesoespecifico_concreto * (espesor_vastago * altura_vastago)
    X_a_vastago = ancho_base - espesor_vastago / 2
    Y_a_vastago = ((altura_base + altura_talon) / 2) + altura_vastago /2
    DC_X_a_vastago = DC_vastago * X_a_vastago
    DC_Y_a_vastago = DC_vastago * Y_a_vastago

    params['DC_vastago'] = round(DC_vastago, 2)
    params['X_a_vastago'] = round(X_a_vastago, 3)
    params['Y_a_vastago'] = round(Y_a_vastago, 3)
    params['DC_X_a_vastago'] = round(DC_X_a_vastago, 2)
    params['DC_Y_a_vastago'] = round(DC_Y_a_vastago, 2)

    DC_espaldar = pesoespecifico_concreto * espesor_espaldar * altura_espaldar
    X_a_espaldar = ancho_base + espesor_espaldar / 2
    Y_a_espaldar = ((altura_base + altura_talon) / 2) + distanciaalabase_espaldar +altura_espaldar / 2 
    DC_X_a_espaldar = DC_espaldar * X_a_espaldar
    DC_Y_a_espaldar = DC_espaldar * Y_a_espaldar

    params['DC_espaldar'] = round(DC_espaldar, 2)
    params['X_a_espaldar'] = round(X_a_espaldar, 3)
    params['Y_a_espaldar'] = round(Y_a_espaldar, 3)
    params['DC_X_a_espaldar'] = round(DC_X_a_espaldar, 2)
    params['DC_Y_a_espaldar'] = round(DC_Y_a_espaldar, 2)

    DC_topes = (pesoespecifico_concreto * cantidad_topes * altura_topes * ancho_topes * largo_topes )/ largo_estribo
    X_a_topes = ancho_base - ancho_topes / 2
    Y_a_topes = ((altura_base + altura_talon) / 2) + altura_vastago + altura_topes / 2
    DC_X_a_topes = DC_topes * X_a_topes
    DC_Y_a_topes = DC_topes * Y_a_topes

    params['DC_topes'] = round(DC_topes, 2)
    params['X_a_topes'] = round(X_a_topes, 3)
    params['Y_a_topes'] = round(Y_a_topes, 3)
    params['DC_X_a_topes'] = round(DC_X_a_topes, 2)
    params['DC_Y_a_topes'] = round(DC_Y_a_topes, 2)

    DC_aletas = pesoespecifico_concreto * cantidad_aletas * (altura_aletas * ancho_aletas - espesor_espaldar * altura_espaldar) * ((espesor_base_aletas + espesor_corona_aletas )/2) / largo_estribo
    X_a_aletas = (ancho_estribo -(ancho_talon-espesor_espaldar)/2)
    Y_a_aletas = ((altura_aletas * espesor_corona_aletas * (altura_aletas /2 + altura_base)) + (0.5 * altura_aletas * (espesor_base_aletas - espesor_corona_aletas ) * (altura_aletas/3 + altura_base))) / ((altura_aletas * espesor_corona_aletas) + 0.5 * altura_aletas *(espesor_base_aletas - espesor_corona_aletas))
    DC_X_a_aletas = DC_aletas * X_a_aletas
    DC_Y_a_aletas = DC_aletas * Y_a_aletas

    params['DC_aletas'] = round(DC_aletas, 2)
    params['X_a_aletas'] = round(X_a_aletas, 3)
    params['Y_a_aletas'] = round(Y_a_aletas, 3)
    params['DC_X_a_aletas'] = round(DC_X_a_aletas, 2)
    params['DC_Y_a_aletas'] = round(DC_Y_a_aletas, 2)

    DC_total_estribo = DC_zapata + DC_vastago + DC_espaldar + DC_topes + DC_aletas
    params['DC_total_estribo'] = round(DC_total_estribo, 2)

    suma_DC_X_a = DC_X_a_zapata + DC_X_a_vastago + DC_X_a_espaldar + DC_X_a_topes + DC_X_a_aletas 
    params['suma_DC_X_a'] = round(suma_DC_X_a, 2)

    suma_DC_Y_a = DC_Y_a_zapata + DC_Y_a_vastago + DC_Y_a_espaldar + DC_Y_a_topes + DC_Y_a_aletas
    params['suma_DC_Y_a'] = round(suma_DC_Y_a, 2)
   
    X_a_estribo = round(suma_DC_X_a / DC_total_estribo, 2)
    params['X_a_estribo'] = X_a_estribo
    
    Y_a_estribo = round(suma_DC_Y_a / DC_total_estribo, 2)
    params['Y_a_estribo'] = Y_a_estribo

    #Carga y momentos debidos al peso propio del relleno
    # DC_relleno: Peso del relleno por m de ancho de estribo, kN/m
    # X_a_relleno: Distancia en el eje x desde el punto A hasta el centro de gravedad de la 'parte de estribo', m 
    # Y_a_relleno: Distancia en el eje y desde el punto A hasta el centro de gravedad de la 'parte de estribo', m
    # DC_X_a_relleno: Momento generado por peso del relleno sobre el punto A, kNm/m
    # DC_Y_a_relleno: Momento generado por peso del relleno sobre el punto A, kNm/m

    DC_relleno = pesoespecifico_suelo * (altura_aletas * ancho_aletas - espesor_espaldar * altura_espaldar)
    params['DC_relleno'] = round(DC_relleno, 2)
    
    X_a_relleno = (ancho_estribo - (ancho_talon - espesor_espaldar) / 2)
    params['X_a_relleno'] = round(X_a_relleno, 2)

    Y_a_relleno = (altura_base + altura_talon) / 2 + altura_aletas / 2
    params['Y_a_relleno'] = round(Y_a_relleno, 2 )

    DC_X_a_relleno = DC_relleno * X_a_relleno
    params['DC_X_a_relleno'] = round(DC_X_a_relleno, 2)

    DC_Y_a_relleno = DC_relleno * Y_a_relleno
    params['DC_Y_a_relleno'] = round(DC_Y_a_relleno, 2)    

    #Sobrecarga LS por carga viva sobre el relleno
    # coeficiente_presion_lateral_suelo: coeficiente de presión lateral del suelo [K]
    # altura_equivalente_suelo: altura equivalente de suelo para carga vehicular, m, Tabla 3.11.6.4.1
    # presion_horizontal_suelo_sobrecargaviva: presión constante horizontal de suelo debida a la sobrecarga por carga viva, Art 3.11.6.4, MPa , Nota: la ecuación descrita en la norma la cual incluye un factor de 10**-9 no tiene sentido físico, por ello no se usa ese factor.
    # L_S_x = componente horizontal de la  presión constante horizontal de suelo debida a la sobrecarga por carga viva por m de ancho de estribo, kN/m
    # M_a_LS_x: Momento de desestabilización en el punto A debido a la sobrecarga por carga viva por m de ancho de estribo, kNm/m
    # L_S_y: componente vertical de la presión constante horizontal de suelo debida a la sobrecarga por carga viva por m de ancho de estribo, kN/m
    # Y_a_LS: longitud cargada con la sobrecarga por carga viva, m
    # M_a_LS_y: Momento de estabilización en el punto A debido a la sobrecarga por carga viva por m de ancho de estribo, kNm/m
     
    coeficiente_presion_lateral_suelo = params['coeficiente_presion_lateral_suelo'] = (1-math.sin(angulodefriccioninternadelsuelodecimentacion/180*math.pi)) / (1+math.sin(angulodefriccioninternadelsuelodecimentacion/180*math.pi))
    if altura_estribo <= 3  : 
        altura_equivalente_suelo = -0.2 * altura_estribo + 1.5
    elif altura_estribo < 6 and altura_estribo > 3 :
        altura_equivalente_suelo = -0.1 * altura_estribo + 1.2
    else :
        altura_equivalente_suelo = 0.6
    
    presion_horizontal_suelo_sobrecargaviva = params['presion_horizontal_suelo_sobrecargaviva'] = round(coeficiente_presion_lateral_suelo * pesoespecifico_suelo * altura_equivalente_suelo, 2) 
    
    params['altura_equivalente_suelo'] = altura_equivalente_suelo

    # componente horizontal y momento de desestabilización en A para la altura total del estribo

    L_S_x = params['L_S_x'] = round(presion_horizontal_suelo_sobrecargaviva * altura_estribo, 2) 
    M_a_LS_x = params['M_a_LS_x'] = round(L_S_x * altura_estribo / 2, 2)

    # Componente vertical y momento de estabilización con respecto al punto A para longitud cargada 
    L_S_y = params['L_S_y'] = round(presion_horizontal_suelo_sobrecargaviva * (ancho_talon - espesor_espaldar), 2)
    Y_a_LS = params['Y_a_LS'] = round((ancho_estribo - (ancho_talon -espesor_espaldar ) / 2), 2)
    M_a_LS_y = params['M_a_LS_y'] = round(L_S_y * Y_a_LS, 2)

    # Acciones verticales por m de estribo
    # suma_cargas_verticales_estribo: cargas verticales totales que actuan sobre el estribo, kN/m
    # suma_M_a_estribo: Momento sobre el punto A debido a las cargas verticales que actuan sobre el estribo, kNm/m 

    suma_cargas_verticales_estribo = params['suma_cargas_verticales_estribo'] = round(DC_total_superestructura_m +DC_total_estribo + DW_m +DC_relleno +carga_vehicular_por_m_ancho_estribo + L_S_y, 2)
    suma_M_a_estribo = params['suma_M_a_estribo'] = round(suma_DC_X_a + M_a_DC +M_a_DW + DC_X_a_relleno + M_a_LLIM + M_a_LS_y, 2)
    
    ## Empuje horizontal del suelo 
    # coeficiente_presion_activa_suelo: coeficiente de presión activa del suelo [Ka]
    # empuje_activo_estatico_EH: empuje activo estático, kN/m
    # Y_a_EH: distancia desde el punto A a la linea de acción de la fuerza resultante del empuje activo, m
    # M_a_EH: Momento de desestabilización producido por el empuje activo EH del terreno, kNm/m
     
    coeficiente_presion_activa_suelo = params['coeficiente_presion_activa_suelo'] = round((1-math.sin(angulodefriccioninternadelsuelodecimentacion/180*math.pi)) / (1+math.sin(angulodefriccioninternadelsuelodecimentacion/180*math.pi)),3)
    empuje_activo_estatico_EH = params['empuje_activo_estatico_EH'] = round(pesoespecifico_suelo * coeficiente_presion_activa_suelo * altura_estribo ** 2 / 2, 2)
    Y_a_EH = params['Y_a_EH'] = round(altura_estribo / 3, 2)
    M_a_EH = params['M_a_EH'] = round(empuje_activo_estatico_EH * Y_a_EH, 2)
    
    ## Fuerzas sismicas
    # F_PGA: factor de sitio en el periodo de vibración cero del espectro de aceleraciones, Tabla 3.10.3.2-1
    # k_h0: Coeficiente sísmico de aceleración horizontal, (suposición que el estribo no se desplaza), Art. 11.6.5.2.1
    # k_h: Coeficiente sísmico de aceleración horizontal, Art. 11.6.5.2.2
    # kv: Coeficiente sísmico de aceleración vertical, Art 11.6.5.2.2
    # beta_estribo: ángulo beta utilizado en el método Mononobe Okabe, Grados, Figura A11.3.1-1
    # delta_estribo: ángulo delta utilizado en el método Mononobe Okabe, Grados, Figura A11.3.1-1
    # i_estribo: ángulo i utilizado en el método Mononobe Okabe, Grados, Figura A11.3.1-1 
    # theta_Mo: ángulo theta_Mo utlizado en el método Mononobe Okabe, Grados, Art A11.3.1-1
    # K_AE: coeficiente de presión sísmica activa del suelo, Art A11.3.1-1
    # P_AE: Fuerza sísmica debida al empuje del terreno por m de estribo, kN/m , Art 11.6.5.3-2
    # delta_P_AE: Diferencia entre el empuje activo estático y el empju del terreno debido al sismo, kN/m
    # distancia_aplicacion_deltaP_AE: distancia de aplicación de delta_P_AE, m, Art A11.3.1
    # M_a_delta_P_AE = Momento producido por delta_P_AE sobre el punto A, kNm/m
    # 
    F_PGA = params['F_PGA'] = params.get('F_PGA',1.05)
    k_h0 = params['k_h0'] = F_PGA * PGA
    k_h = params['k_h'] = 0.5 * k_h0

    kv = params['kv'] = params.get('kv',0)
    beta_estribo = params['beta_estribo'] = params.get('beta_estribo',0)
    delta_estribo = params['delta_estribo'] = params.get('delta_estribo', 0)
    i_estribo = params['i_estribo'] = params.get('i_estribo',0)
   
    theta_Mo = params['theta_Mo'] = round(math.atan(k_h/(1-kv)) *180 / math.pi, 2)
    
    K_AE = params['K_AE']= round((math.cos((angulodefriccioninternadelsuelodecimentacion-theta_Mo-beta_estribo)* math.pi /180 )) ** 2 / ((math.cos(theta_Mo /180 * math.pi)) * (math.cos(beta_estribo * math.pi/ 180)) **2 * math.cos((delta_estribo + beta_estribo +theta_Mo)/180* math.pi)) * (1+ math.sqrt((math.sin((angulodefriccioninternadelsuelodecimentacion + delta_estribo)/180*math.pi)*math.sin((angulodefriccioninternadelsuelodecimentacion - theta_Mo - i_estribo)/180* math.pi))/(math.cos((delta_estribo +beta_estribo + theta_Mo)/180*math.pi)*math.cos((i_estribo - beta_estribo)/180*math.pi))))**-2, 3)
    P_AE = params['P_AE'] = round(0.5 * K_AE * pesoespecifico_suelo * altura_estribo ** 2, 2)
    delta_P_AE = params['delta_P_AE'] = round(P_AE - empuje_activo_estatico_EH, 2)
    distancia_aplicacion_deltaP_AE = params['distancia_aplicacion_deltaP_AE'] = round(0.4 * altura_estribo, 2)
    M_a_delta_P_AE = params['M_a_delta_P_AE'] = round(delta_P_AE * distancia_aplicacion_deltaP_AE, 2)

    # Calculo de fuerza PIR
    # P_IR: Fuerza horizontal debida a la fuerza sísmica de la masa del muro, kN/m, Art 11.6.5.1-1
    P_IR = params['P_IR'] = round(k_h *( DC_relleno + DC_total_estribo), 2)
    

    # Combinacion mas desfavorble de fuerzas debidas al sismo
    # Pseis_1: combinación: 100% del empuje activo sísmico + 50% de la fuerza sísmica debida al peso del suelo de relleno, kN
    # Pseis_2: combinación: 50% del empuje activo sísmico + 100% de la fuerza sísmica debida al peso del suelo de relleno, kN
    # Pseis_e: Combinación de mayor valor , kN
    # M_a_P_seis: Momento producido por P_seis sobre el punto A, kNm/m

    Pseis_1 = params['Pseis_1'] = round(delta_P_AE + 0.5 * P_IR, 2)
    Pseis_2 = params['Pseis_2'] = round(0.5* empuje_activo_estatico_EH + P_IR, 2)

    if Pseis_1 > Pseis_2 :
        Pseis_e =  Pseis_1
    else :
        Pseis_e = Pseis_2
    M_a_p_seis = params['M_a_p_seis'] = round(distancia_aplicacion_deltaP_AE * Pseis_e, 2)

    params['Pseis_e'] = round(Pseis_e, 2)

    #Fuerza sismica Hbu proveniente de la superestructura
    # coeficiente_friccion: Coeficiente de fricción, 0.2 valor promedio empleado para dispositivos elastoméricos apoyados sobre concreto y acero
    #
    # P_u: Fuerza de compresión, obtenida a partir de combinaciones de resistencia y evento extremo, kN/m, Tabla 3.4.1-1
    # Hbu: Carga lateral transmitida a la superestructura y a la infraestructura por los apoyos, kN/m, Art 14.6.3.1-1
    # distancia_aplicacion_Hbu: La fuerza Hbu se aplica a la altura del apoyo de las vigas, m
    # M_a_Hbu: Momento de desestbilización de la fuerza horizontal Hbu, con respecto al punto A, kNm/m
    # suma_fuerzas_sismicas: Sumatoria de fuerzas sísmicas (Pseis y Hbu), kN/m
    # suma_M_a_fuerzas_sismicas: Sumatoria de momentos respecto al punto A debidos a fuerzas sísmicas, kNm/m
    
    coeficiente_friccion = params['coeficiente_friccion'] = params.get('coeficiente_friccion', 0.2)
    P_u = params['P_u'] = round(1.25 * DC_total_superestructura_m + 1.5 * DW_m + 0.5 * carga_vehicular_por_m_ancho_estribo,2)
    Hbu =params['Hbu'] = round(coeficiente_friccion * P_u, 2)
    distancia_aplicacion_Hbu = params['distancia_aplicacion_Hbu'] = round(altura_base + altura_vastago, 2)
    M_a_Hbu = params['M_a_Hbu'] = round(distancia_aplicacion_Hbu * Hbu, 2)


    suma_fuerzas_sismicas = params['suma_fuerzas_sismicas'] = round(Pseis_e + Hbu, 2)
    suma_M_a_fuerzas_sismicas = params['suma_M_a_fuerzas_sismicas'] = round(M_a_p_seis + M_a_Hbu, 2)
    
    #Longitud de apoyo

    S_angulo_sesgo = params['S_angulo_sesgo'] = params.get('S_angulo_sesgo',0 )
    altura_columnas = params['altura_columnas'] = params.get('altura_columnas', 0 )
    mayoración_N = params['mayoracion_N'] = params.get('mayoracion_N', 1.5 ) 
    longitud_apoyo = params['longitud_apoyo'] = round(mayoración_N * ((200 + 0.0017 * L_superestructura * 1000 + 0.0067 * altura_columnas * 1000) + (1 + 0.000125 * (S_angulo_sesgo * 1000) ** 2))/1000, 2)
    
    if longitud_apoyo > espesor_vastago :
        print('No cumple longitud de apoyo')
    
    #Verificacion por estabilidad al volcamiento y al deslizamiento
    # factor_carga_[ ]_max: Factor de carga máximo para el tipo de carga especificado, Tabla 3.4.1.2 
    # factor_carga_[ ]_min: Factor de carga mínimo para el tipo de carga especificado, Tabla 3.4.1.2
    # fuerza_max_vertical_[]: Combinación máxima de fuerzas para el estado límite especificado, kN/m    
    # fuerza_min_vertical_[]: Combinación mínima de fuerzas para el estado límite especificado, kN/m
    # momento_max_vertical_[]: Combinación máxima de momentos para el estado límite especificado, kNm/m    
    # momento_min_vertical_[]: Combinación mínima de momentos para el estado límite especificado, kNm/m  
    # fuerza_max_horizontal_[]: Combinación máxima de fuerzas para el estado límite especificado, kN/m    
    # fuerza_min_horizontal_[]: Combinación mínima de fuerzas para el estado límite especificado, kN/m
    # momento_max_horizontal_[]: Combinación máxima de momentos para el estado límite especificado, kNm/m    
    # momento_min_horizontal_[]: Combinación mínima de momentos para el estado límite especificado, kNm/m 

    factor_carga_DC_max = params['factor_carga_DC_max'] = params.get('factor_carga_DC_max', 1.25)
    factor_carga_DC_min = params['factor_carga_DC_min'] = params.get('factor_carga_DC_min', 0.9)
    factor_carga_DW_max = params['factor_carga_DW_max'] = params.get('factor_carga_DW_max', 1.5)
    factor_carga_DW_min = params['factor_carga_DW_min'] = params.get('factor_carga_DW_min', 0.65)
    factor_carga_EH_max = params['factor_carga_EH_max'] = params.get('factor_carga_EH_max', 1.5)
    factor_carga_EH_min = params['factor_carga_EH_min'] = params.get('factor_carga_EH_min', 0.9)
    factor_carga_EV_eg_max = params['factor_carga_EV_max'] = params.get('factor_carga_EV_max', 1)
    factor_carga_EV_eg_min = params['factor_carga_EV_min'] = params.get('factor_carga_EV_min', 0)    
    factor_carga_EV_MyE_max = params['factor_carga_EV_MyE_max'] = params.get('factor_carga_EV_MyE_max', 1.35)
    factor_carga_EV_MyE_min = params['factor_carga_EV_MyE_min'] = params.get('factor_carga_EV_MyE_min', 1)
    factor_carga_ES_max = params['factor_carga_ES_max'] = params.get('factor_carga_ES_max', 1.5)
    factor_carga_ES_min = params['factor_carga_ES_min'] = params.get('factor_carga_ES_min', 0.75)
    factor_carga_EQ_max = params['factor_carga_EQ_max'] = params.get('factor_carga_EQ_max', 1)
    factor_carga_EQ_min = params['factor_carga_EQ_min'] = params.get('factor_carga_EQ_min', 1)
    factor_carga_LS_max = params['factor_carga_LS_max'] = params.get('factor_carga_LS_max', 1.75)
    factor_carga_LS_min = params['factor_carga_LS_min'] = params.get('factor_carga_LS_min', 0)
    factor_carga_LS_EE_max = params['factor_carga_LS_EE_max'] = params.get('factor_carga_LS_EE_max', 0.5)
    factor_carga_LS_EE_min = params['factor_carga_LS_EE_min'] = params.get('factor_carga_LS_EE_min', 0)
    
    fuerza_max_vertical_resistencia = params['fuerza_max_vertical_resistencia'] = round(factor_carga_DC_max * DC_total_superestructura_m + factor_carga_DC_max * DC_total_estribo + factor_carga_DW_max * DW_m + factor_carga_EV_MyE_max * DC_relleno + factor_carga_LS_max * carga_vehicular_por_m_ancho_estribo + factor_carga_LS_max * L_S_y, 2)
    fuerza_min_vertical_resistencia = params['fuerza_min_vertical_resistencia'] = round(factor_carga_DC_min * DC_total_superestructura_m + factor_carga_DC_min * DC_total_estribo + factor_carga_DW_min * DW_m + factor_carga_EV_MyE_min * DC_relleno + factor_carga_LS_min * carga_vehicular_por_m_ancho_estribo + factor_carga_LS_min * L_S_y, 2)
    fuerza_max_vertical_eventoextremo = params['fuerza_max_vertical_eventoextremo'] = round(factor_carga_DC_max * DC_total_superestructura_m + factor_carga_DC_max * DC_total_estribo + factor_carga_DW_max * DW_m + factor_carga_EV_MyE_max * DC_relleno + factor_carga_LS_EE_max * carga_vehicular_por_m_ancho_estribo + factor_carga_LS_EE_max * L_S_y, 2)
    fuerza_min_vertical_eventoextremo = params['fuerza_min_vertical_eventoextremo'] = round(factor_carga_DC_min * DC_total_superestructura_m + factor_carga_DC_min * DC_total_estribo + factor_carga_DW_min * DW_m + factor_carga_EV_MyE_min * DC_relleno + factor_carga_LS_EE_min * carga_vehicular_por_m_ancho_estribo + factor_carga_LS_EE_min * L_S_y, 2)
    fuerza_vertical_servicio = params['fuerza_vertical_servicio'] = round( DC_total_superestructura_m +  DC_total_estribo + DW_m + DC_relleno + carga_vehicular_por_m_ancho_estribo + L_S_y, 2)

    momento_max_vertical_resistencia = params['momento_max_vertical_resistencia'] = round( factor_carga_DC_max * M_a_DC + factor_carga_DC_max * suma_DC_X_a + factor_carga_DW_max * M_a_DW + factor_carga_EV_MyE_max * DC_X_a_relleno + factor_carga_LS_max * M_a_LLIM + factor_carga_LS_max * M_a_LS_y ,2)
    momento_min_vertical_resistencia = params['momento_min_vertical_resistencia'] = round( factor_carga_DC_min * M_a_DC + factor_carga_DC_min * suma_DC_X_a + factor_carga_DW_min * M_a_DW + factor_carga_EV_MyE_min * DC_X_a_relleno + factor_carga_LS_min * M_a_LLIM + factor_carga_LS_min * M_a_LS_y ,2)
    momento_max_vertical_eventoextremo = params['momento_max_vertical_eventoextremo'] = round( factor_carga_DC_max * M_a_DC + factor_carga_DC_max * suma_DC_X_a + factor_carga_DW_max * M_a_DW + factor_carga_EV_MyE_max * DC_X_a_relleno + factor_carga_LS_EE_max * M_a_LLIM + factor_carga_LS_EE_max * M_a_LS_y ,2)
    momento_min_vertical_eventoextremo = params['momento_min_vertical_eventoextremo'] = round( factor_carga_DC_min * M_a_DC + factor_carga_DC_min * suma_DC_X_a + factor_carga_DW_min * M_a_DW + factor_carga_EV_MyE_min * DC_X_a_relleno + factor_carga_LS_EE_min * M_a_LLIM + factor_carga_LS_EE_min * M_a_LS_y ,2)
    momento_vertical_servicio = params['momento_vertical_servicio'] = round( M_a_DC + suma_DC_X_a + M_a_DW + DC_X_a_relleno + M_a_LLIM + M_a_LS_y ,2)

    fuerza_max_horizontal_resistencia = params['fuerza_max_horizontal_resistencia'] = round( factor_carga_EH_max * empuje_activo_estatico_EH + factor_carga_LS_max * (L_S_x + BR_m_ancho) , 2)
    fuerza_min_horizontal_resistencia = params['fuerza_min_horizontal_resistencia'] = round( factor_carga_EH_min * empuje_activo_estatico_EH + factor_carga_LS_min * (L_S_x + BR_m_ancho) , 2)
    fuerza_max_horizontal_eventoextremo = params['fuerza_max_horizontal_eventoextremo'] = round( factor_carga_EH_max * empuje_activo_estatico_EH + factor_carga_LS_EE_max * (L_S_x + BR_m_ancho) + factor_carga_EQ_max * Pseis_e + factor_carga_EQ_max * Hbu, 2)
    fuerza_min_horizontal_eventoextremo = params['fuerza_min_horizontal_eventoextremo'] = round( factor_carga_EH_min * empuje_activo_estatico_EH + factor_carga_LS_EE_min * (L_S_x + BR_m_ancho) + factor_carga_EQ_min * Pseis_e + factor_carga_EQ_min * Hbu, 2)
    fuerza_horizontal_servicio = params['fuerza_horizontal_servicio'] = round( empuje_activo_estatico_EH + L_S_x + BR_m_ancho, 2)

    momento_max_horizontal_resistencia = params['momento_max_horizontal_resistencia'] = round( factor_carga_EH_max * M_a_EH + factor_carga_LS_max * (M_a_LS_x + M_a_BR) , 2)
    momento_min_horizontal_resistencia = params['momento_min_horizontal_resistencia'] = round( factor_carga_EH_min * M_a_EH + factor_carga_LS_min * (M_a_LS_x + M_a_BR) , 2)
    momento_max_horizontal_eventoextremo = params['momento_max_horizontal_eventoextremo'] = round( factor_carga_EH_max * M_a_EH + factor_carga_LS_EE_max * (M_a_LS_x+M_a_BR) + factor_carga_EQ_max * M_a_p_seis + factor_carga_EQ_max * M_a_Hbu, 2)
    momento_min_horizontal_eventoextremo = params['momento_min_horizontal_eventoextremo'] = round( factor_carga_EH_min * M_a_EH + factor_carga_LS_EE_min * (M_a_LS_x+M_a_BR) + factor_carga_EQ_min * M_a_p_seis + factor_carga_EQ_min * M_a_Hbu, 2)
    momento_horizontal_servicio = params['momento_horizontal_servicio'] = round( M_a_EH + M_a_LS_x + M_a_BR, 2) 
    
    # Verificación al volcamiento
    # d_[]_[]: distancia de aplicación de la resultante vertical respecto al punto A para el caso de solicitciones [máximas o  mínimas] en el estado de límite especificado, m
    # e_max_resistencia: excentricidad medida desde el centro de la base del estribo para el caso de solicitciones [máximas o mínimas] en el estado de límite especificado, m
    # e_limite_resistencia: excentricidad máxima definida según Art 11.6.3.3, m
    # e_limite_eventoextremo: excentricidad máxima definida según Art 11.6.5, m
    

    d_max_resistencia = params['d_max_resistencia'] = round((momento_max_vertical_resistencia - momento_max_horizontal_resistencia)/fuerza_max_vertical_resistencia, 2)
    e_max_resistencia = params['e_max_resistencia'] = round(ancho_estribo / 2 - d_max_resistencia, 2)
   
    if tipodesuelo == 'no rocoso':
       e_limite_resistencia = round(ancho_estribo/3, 2)
    else :
        e_limite_resistencia = round(4.5 * ancho_estribo/10, 2)
    params['e_limite_resistencia'] = e_limite_resistencia 
   
    if math.fabs(e_max_resistencia) > e_limite_resistencia:
        print('no cumple verificación al volcamiento, estado límite resistencia')

    d_min_resistencia = params['d_min_resistencia'] = round((momento_min_vertical_resistencia - momento_min_horizontal_resistencia)/fuerza_min_vertical_resistencia, 2)
    e_min_resistencia = params['e_min_resistencia'] = round(ancho_estribo / 2 - d_min_resistencia, 2)
   
    if math.fabs(e_min_resistencia) > e_limite_resistencia:
        print('no cumple verificación al volcamiento, estado límite resistencia')

    d_max_eventoextremo = params['d_max_eventoextremo'] = round((momento_max_vertical_eventoextremo - momento_max_horizontal_eventoextremo)/fuerza_max_vertical_eventoextremo, 2)
    e_max_eventoextremo = params['e_max_eventoextremo'] = round(ancho_estribo / 2 - d_max_eventoextremo, 2)
   
    if factor_carga_LS_EE_max == 0 :
       e_limite_eventoextremo = round(ancho_estribo/3, 2)
    elif factor_carga_LS_EE_max == 1 :
        e_limite_eventoextremo = round(4* ancho_estribo/10, 2)
    elif 0 < factor_carga_LS_EE_max < 1:
        e_limite_eventoextremo = ancho_estribo/3 + (ancho_estribo/15 * factor_carga_LS_EE_max)
        
    params['e_limite_eventoextremo'] = e_limite_eventoextremo 
   
    if math.fabs(e_max_eventoextremo > e_limite_eventoextremo):
        print('no cumple verificación al volcamiento, estado límite resistencia')

    d_min_eventoextremo = params['d_min_eventoextremo'] = round((momento_min_vertical_eventoextremo - momento_min_horizontal_eventoextremo)/fuerza_min_vertical_eventoextremo, 2)
    e_min_eventoextremo = params['e_min_eventoextremo'] = round(ancho_estribo / 2 - d_min_eventoextremo, 2)
   
    if math.fabs(e_min_eventoextremo) > e_limite_eventoextremo:
        print('no cumple verificación al volcamiento, estado límite resistencia')    
    
    # Verificación de los esfuerzos sobre el suelo
    # esfuerzo_suelo_[]_[]: esfuerzo verical sobre el área efectiva de la base para el caso [máximo o mínimo] del estado limite especificado, MPa

    esfuerzo_suelo_max_resistencia = params['esfuerzo_suelo_max_resistencia'] = round(fuerza_max_vertical_resistencia / ( ancho_estribo - 2* math.fabs(e_max_resistencia))/1000, 2)
    if esfuerzo_suelo_max_resistencia > capacidadportantemayoradadelsuelo :
        print('no cumple verificación de esfuerzos sobre el suelo, estado límite resistencia') 
    
    esfuerzo_suelo_min_resistencia = params['esfuerzo_suelo_min_resistencia'] = round(fuerza_min_vertical_resistencia / ( ancho_estribo - 2* math.fabs(e_min_resistencia))/1000, 2)
    if esfuerzo_suelo_min_resistencia > capacidadportantemayoradadelsuelo :
        print('no cumple verificación de esfuerzos sobre el suelo, estado límite resistencia') 
    
    esfuerzo_suelo_max_eventoextremo = params['esfuerzo_suelo_max_eventoextremo'] = round(fuerza_max_vertical_eventoextremo / ( ancho_estribo - 2* math.fabs(e_max_eventoextremo))/1000, 2)
    if esfuerzo_suelo_max_eventoextremo > capacidadportantemayoradadelsuelo_eventoextremo :
        print('no cumple verificación de esfuerzos sobre el suelo, estado límite eventoextremo') 
    
    esfuerzo_suelo_min_eventoextremo = params['esfuerzo_suelo_min_eventoextremo'] = round(fuerza_min_vertical_eventoextremo / ( ancho_estribo - 2* math.fabs(e_min_eventoextremo))/1000, 2)
    if esfuerzo_suelo_min_eventoextremo > capacidadportantemayoradadelsuelo_eventoextremo :
        print('no cumple verificación de esfuerzos sobre el suelo, estado límite eventoextremo') 
   
    d_servicio = params['d_servicio'] = round((momento_vertical_servicio - momento_horizontal_servicio)/fuerza_vertical_servicio, 2)
    e_servicio = params['e_servicio'] = round(ancho_estribo / 2 - d_servicio, 2)

    esfuerzo_suelo_servicio = params['esfuerzo_suelo_servicio'] = round(fuerza_vertical_servicio / ( ancho_estribo - 2* math.fabs(e_servicio))/1000, 2)
    if esfuerzo_suelo_servicio > capacidadportantemayoradadelsuelo_servicio :
        print('no cumple verificación de esfuerzos sobre el suelo, estado límite servicio') 
    
    
    #Verifificación cuando el estribo es soportado sobre roca
    # d_[]_resistencia_roca: distancia de aplicación de la resultante vertical respecto al punto A para el caso de solicitciones [máximas o  mínimas] en el estado de límite especificado en cimentación sobre roca, m
    # e_[]_resistencia_roca: e_max_resistencia: excentricidad medida desde el centro de la base del estribo para el caso de solicitciones [máximas o mínimas] en el estado de límite especificado, m
    # esfuerzo_suelo_[]_resistencia_roca_max: esfuerzo máximo vertical del suelo rocoso, MPa
    # esfuerzo_suelo_[]_resistencia_roca_min: esfuerzo mínimo vertical del suelo rocoso, MPa
    
    d_max_resistencia_roca = params['d_max_resistencia_roca'] = (momento_max_vertical_resistencia - momento_max_horizontal_resistencia) / fuerza_max_vertical_resistencia
    d_min_resistencia_roca = params['d_min_resistencia_roca'] = (momento_min_vertical_resistencia - momento_min_horizontal_resistencia) / fuerza_min_vertical_resistencia

    e_max_resistencia_roca = params['e_max_resistencia_roca'] = (ancho_estribo/2 - d_max_resistencia_roca)
    e_min_resistencia_roca = params['e_min_resistencia_roca'] = (ancho_estribo/2 - d_min_resistencia_roca) 

    if math.fabs(e_max_resistencia_roca) > ancho_estribo/6 :
        esfuerzo_suelo_max_resistencia_roca_max = (2 * fuerza_max_vertical_resistencia)/(3*ancho_estribo * (ancho_estribo / 2 - e_max_resistencia_roca));
        esfuerzo_suelo_max_resistencia_roca_min = 0
        
        if math.fabs(e_max_resistencia_roca) > 9 * ancho_estribo /20:   
            print('no cumple ubicación de excentricicdad para esfuerzo sobre roca')
    else :
        esfuerzo_suelo_max_resistencia_roca_max = (fuerza_max_vertical_resistencia / ancho_estribo) * (1 + 6 * e_max_resistencia_roca / ancho_estribo)
        esfuerzo_suelo_max_resistencia_roca_min = (fuerza_max_vertical_resistencia / ancho_estribo) * (1 - 6 * e_max_resistencia_roca / ancho_estribo)
    
    
    if math.fabs(e_min_resistencia_roca) > ancho_estribo/6 :
        esfuerzo_suelo_min_resistencia_roca_max = (2 * fuerza_min_vertical_resistencia)/(3*ancho_estribo * (ancho_estribo / 2 - e_min_resistencia_roca))
        esfuerzo_suelo_min_resistencia_roca_min = 0
        
        if math.fabs(e_min_resistencia_roca) > 9 * ancho_estribo /20:   
            print('no cumple ubicación de excentricicdad para esfuerzo sobre roca')
    else :
        esfuerzo_suelo_min_resistencia_roca_max = (fuerza_min_vertical_resistencia / ancho_estribo) * (1 + 6 * e_min_resistencia_roca / ancho_estribo)
        esfuerzo_suelo_min_resistencia_roca_min = (fuerza_min_vertical_resistencia / ancho_estribo) * (1 - 6 * e_min_resistencia_roca / ancho_estribo)

    params['esfuerzo_suelo_max_resistencia_roca_max'] = esfuerzo_suelo_max_resistencia_roca_max
    params['esfuerzo_suelo_max_resistencia_roca_min'] = esfuerzo_suelo_max_resistencia_roca_min
    
    params['esfuerzo_suelo_min_resistencia_roca_max'] = esfuerzo_suelo_min_resistencia_roca_max
    params['esfuerzo_suelo_min_resistencia_roca_min'] = esfuerzo_suelo_min_resistencia_roca_min
    
    # Verificación de desplazamiento del estribo
    # factor_resistencia_cortante_suelo_cimentacion: Factor de resistencia para la resistencia al cortante entre el suelo y la cimentación, Tabla 10.5.5.2.2-1
    # tipo_de_concreto_zapata: defiinición de la elaboración del concreto de la zapata [ in situ o  prefabricado]
    # factor_tipo_concreto_zapata: factor utilizado en 10.6.3.4-2 según el tipo de concreto de la zapata.
    # resistencia_nominal_desplazamiento_[]_[]: Resistencia nominal de deslizamiento contra la falla por deslizamiento, Art 10.6.3.4, kN.

    
    factor_resistencia_cortante_suelo_cimentacion = params['factor_resistencia_cortante_suelo_cimentacion'] = params.get('factor_resistencia_cortante_suelo_cimentacion', 0.8)
    
    tipo_de_concreto_zapata = params['tipo_de_concreto_zapata'] = params.get('tipo_de_concreto_zapata', 'in situ') 

    if tipo_de_concreto_zapata == 'prefabricado':
        factor_tipo_concreto_zapata = 0.8
    else :
        factor_tipo_concreto_zapata = 1
    params['tipo_de_concreto_zapata']  = tipo_de_concreto_zapata

    resistencia_nominal_desplazamiento_max_resistencia = params['resistencia_nominal_desplazamiento_max_resistencia'] = round(fuerza_max_vertical_resistencia *factor_resistencia_cortante_suelo_cimentacion * factor_tipo_concreto_zapata *math.tan(angulodefriccioninternadelsuelodecimentacion/180* math.pi),2)
    resistencia_nominal_desplazamiento_min_resistencia = params['resistencia_nominal_desplazamiento_min_resistencia'] = round(fuerza_min_vertical_resistencia *factor_resistencia_cortante_suelo_cimentacion * factor_tipo_concreto_zapata * math.tan(angulodefriccioninternadelsuelodecimentacion/180* math.pi),2)
    resistencia_nominal_desplazamiento_max_eventoextremo = params['resistencia_nominal_desplazamiento_max_eventoextremo'] = round(fuerza_max_vertical_eventoextremo *factor_resistencia_cortante_suelo_cimentacion * factor_tipo_concreto_zapata * math.tan(angulodefriccioninternadelsuelodecimentacion/180* math.pi),2)
    resistencia_nominal_desplazamiento_min_eventoextremo = params['resistencia_nominal_desplazamiento_min_eventoextremo'] = round(fuerza_min_vertical_eventoextremo *factor_resistencia_cortante_suelo_cimentacion * factor_tipo_concreto_zapata * math.tan(angulodefriccioninternadelsuelodecimentacion/180* math.pi),2)
    
    if fuerza_max_horizontal_resistencia > resistencia_nominal_desplazamiento_max_resistencia :
        print('no cumple resistencia al desplazamiento, caso máximo, resistencia')
    
    if fuerza_min_horizontal_resistencia > resistencia_nominal_desplazamiento_min_resistencia :
        print('no cumple resistencia al desplazamiento, caso mínimo, resistencia')
    if fuerza_max_horizontal_eventoextremo > resistencia_nominal_desplazamiento_max_eventoextremo :
        print('no cumple resistencia al desplazamiento, caso máximo, evento extremo')
    if fuerza_min_horizontal_eventoextremo > resistencia_nominal_desplazamiento_min_eventoextremo :
        print('no cumple resistencia al desplazamiento, caso mínimo, evento extremo')
    

    ## DISEÑO DE VASTAGO
    # Diseño de la armadura interior del vástago

    # EH_vastago: Empuje estático del suelo sobre el vástago, kN/m
    # Y_vastago_EH: Distancia de aplicación de la resultante de EH_vastago desde la unión vástago - zapata. m
    # Y_vastago_pseis: Distancia de aplicación de la fuerza Pseis desde la unión vástago - zapata. m
    # Y_vastago_Hbu: Distancia de aplicación de la fuerza Hbu desde la unión vástago - zapata. m
    # Y_vastago_BR: Distancia de aplicación de la fuerza BR desde la unión vástago - zapata. m
    # Y_vastago_LSy: Distancia de aplicación de fuerza LSy desde la unión vástago - zapata. m
    # M_a_a_[]_vastago: Momento producido por la fuerza [] en la unión vástago zapata, kNm/m


    EH_vastago = params['EH_vastago'] = round(0.5 * coeficiente_presion_activa_suelo * pesoespecifico_suelo * (altura_estribo - altura_base) ** 2, 2)
    Y_vastago_EH = params['Y_vastago_EH'] = round((altura_estribo - altura_base) / 3 ,2)
    Y_vastago_pseis = params['Y_vastago_pseis'] =round(0.4 * (altura_estribo - altura_base), 2)
    Y_vastago_Hbu = params['Y_vastago_Hbu'] = altura_vastago 
    Y_vastago_BR = params['Y_vastago_BR'] = round(altura_vastago + 1.8 , 2)
    L_S_y_vastago = params['L_S_y_vastago'] = round(presion_horizontal_suelo_sobrecargaviva * (altura_estribo - altura_base),2)
    Y_vastago_LSy = params['Y_vastago_LSy'] =round((altura_estribo - altura_base)/2 ,2)
    M_a_a_EH_vastago = params['M_a_a_EH_vastago'] =round(EH_vastago * Y_vastago_EH, 2)
    M_a_a_pseis_vastago = params['M_a_a_pseis_vastago'] = round( Pseis_e * Y_vastago_pseis ,2) 
    M_a_a_Hbu_vastago = params['M_a_a_Hbu_vastago'] = round( Hbu * Y_vastago_Hbu ,2) 
    M_a_a_BR_vastago = params['M_a_a_BR_vastago'] = round( BR_m_ancho * Y_vastago_BR ,2) 
    M_a_a_LSy_vastago = params['M_a_a_LSy_vastago'] = round( L_S_y_vastago * Y_vastago_LSy ,2) 

    # Momento mayorado Evento extemo I
    # Mu_vastago_[]: Momento último de diseño para el estado límite especificado. kNm/m
    # Mu_vastago_diseño: El mayor entre los momentos últimos de resistencia y evento extremo. kNm/m
    # recub_vastago: recubrimiento de concreto del vástago, m
    # phi_vastago: factor phi utilizado en la ecuación de la cuantía.
    # d_vastago: distancia desde la cara superior hasta el centroide del acero a tracción, m
    # cuantía_vastago: Cuantia de acero a flexión para el vástago.
    # As_flexion_vastago: Área de acero para flexión por m de ancho de vástago, cm2
    # As_8: Área de una barra #8, cm2.
    # No_barras_8_flexion_vastago: Número de barras #8 necesarias paea cumplir el área de acero requerida. 
    # separacion_flexion_vastago: Separación entre barras en el vástago para el diseño a flexión, cm

    
    Mu_vastago_eventoextremo = params['Mu_vastago_eventoextremo'] = round(1.5 * M_a_a_EH_vastago + 1 * (M_a_a_pseis_vastago + M_a_a_Hbu_vastago), 2) 
    Mu_vastago_resistencia = params['Mu_vastago_resistencia'] = round(1.5 * M_a_a_EH_vastago + 1.75 *(M_a_a_LSy_vastago + M_a_a_BR_vastago), 2)

    if Mu_vastago_eventoextremo > Mu_vastago_resistencia:
        Mu_vastago_diseño = Mu_vastago_eventoextremo
    else :
        Mu_vastago_diseño = Mu_vastago_resistencia
    
    params['Mu_vastago_diseño'] = Mu_vastago_diseño
  
    recub_vastago = params['recub_vastago'] = params.get('recub_vastago', 0.08)
    phi_vastago = params['phi_vastago'] = params.get('phi_vastago', 0.9)
    d_vastago = params['d_vastago'] = round( espesor_vastago - recub_vastago ,2)
   
    cuantia_vastago_flexion = params['cuantia_vastago_flexion'] = round((1-(1-(2 * Mu_vastago_diseño / (phi_vastago * 1 * d_vastago ** 2 * 0.85 * fc_estribo *1000))) ** 0.5) * 0.85* fc_estribo / fy , 5)
    As_flexion_vastago = params['As_flexion_vastago'] = round(cuantia_vastago_flexion * d_vastago *100 * 100, 2)
    As_8 = params['As_8'] = 5.1
    No_barras_8_flexion_vastago = params['No_barras_8_flexion_vastago'] = round(As_flexion_vastago / As_8, 2)
    separacion_flexion_vastago = params['separacion_flexion_vastago'] = round(100/ No_barras_8_flexion_vastago)
    
    #Verificación armadura mínima del vástago
    # gamma_3: relación entre la resistencia especificada a fluencia y la resistencia última a tracción del refuerzo. Art 5.7.3.3.2
    # gamma_1: factor de variación de la fisuración por flexión, Art 5.7.3.3.2
    # fr_vastago: Módulo de rotura del concreto en el vástago, Art 5.4.2.6, MPa
    # Sc_vastago: Módulo de sección para la fibra extrema de la sección compuesta donde el esfuerzo es causado por las cargas externas. m3 
    # MCR_vastago: Momento de verificación de refuerzo mínimo, Art 5.7.3.3.2, kNm
    
    gamma_3_vastago = params['gamma_3_vastago'] = params.get('gamma_3_vastago', 0.75)
    gamma_1_vastago = params['gamma_1_vastago'] = params.get('gamma_1_vastago', 1.6)
    fr_vastago = params['fr_vastago'] = round(0.62 * (fc_estribo)**0.5, 2)
    Sc_vastago = params['Sc_vastago'] = round(1*espesor_vastago ** 2 / 6, 2)
    MCR_vastago = params['MCR_vastago'] = round(gamma_3_vastago * (gamma_1_vastago ** 2 * fr_vastago * Sc_vastago)*1000, 2)
    if MCR_vastago > Mu_vastago_diseño :
        print('no cumple armadura mínima en el vástago')
    
    #Armadura por retracción de fraguado y temperatura en el cuerpo del vástago
    #
    # As_retraccionytemperatura_vastago: Área de refuerzo por retracción y temperatura, mm2, Art 5.10.8
    # As_4: Área de una barra #4, cm2
    # No_barras_4_retraccionytemperatura_vastago: Número de barras necesarias para cumplir el refuerzo minimo por retracción de fraguado y temperatura.
    # separacion_retraccionytemperatura_vastago: separación de las barras de refuerzo por retracción de fraguado y temperatura, cm  

    As_retraccionytemperatura_vastago = params['As_retraccionytemperatura_vastago'] = round(750 * altura_vastago * espesor_vastago *1000 /( 2 * (altura_vastago + espesor_vastago) * fy),2)
    if As_retraccionytemperatura_vastago < 234 or As_retraccionytemperatura_vastago > 1278 :
        print( 'no cumple armadura por retracción y temperatura' )
    As_4 = params['As_4'] = 1.29
    No_barras_4_retraccionytemperatura_vastago = params['No_barras_4_retraccionytemperatura_vastago'] = math.ceil(As_retraccionytemperatura_vastago /100 / As_4)
    separacion_retraccionytemperatura_vastago = params['separacion_retraccionytemperatura_vastago'] = round(100 / No_barras_4_retraccionytemperatura_vastago, 2)
    
    # Control de agrietamiento del acero del vástago

    # gamma_e_vastago: Factor de exposición según Art 5.7.3.4
    #
    # relacionmodular_estribo: relación entre el módulo de elasticidad del acero y el modulo de elasticidad del concreto
    # M_servicio_vastago: Momento para el estado límite de servicio, kNm/m
    # X_ejecentroidal_vastago: Posición del eje centroidal de la sección transformada, m
    # I_vastago: Momento centroidal de inercia de la sección transformada, m4
    # fss_vastago: Esfuerzo actuante sobre el acero de refuerzo, MPa
    # beta_s_vastago: coeficiente definido en Art 5.7.3.4-1
    # separacion_maxima_agrietamiento_vastago: Separación máxima del refuerzo a tracción, Art 5.7.3.4, cm.


    gamma_e_vastago = params['gamma_e_vastago'] = params.get('gamma_e_vastago', 1)
    relacionmodular_estribo = params['relacionmodular_estribo'] = round(E_acero / (4800 * (fc_estribo)** 0.5))   
    M_servicio_vastago =params['M_servicio_vastago']= M_a_a_EH_vastago + 1 * (M_a_a_BR_vastago + M_a_a_LSy_vastago) 
    X_ejecentroidal_vastago = params['X_ejecentroidal_vastago'] = round(- 2 * relacionmodular_estribo * As_flexion_vastago /10000 + ((2 * relacionmodular_estribo * As_flexion_vastago /10000)**2 - 4 * 1* -2 * relacionmodular_estribo * As_flexion_vastago /10000 *d_vastago)**0.5 /( 2 * 1),2)
    I_vastago = params['I_vastago'] = round(1 * X_ejecentroidal_vastago ** 3 / 3 + relacionmodular_estribo * As_flexion_vastago /10000 * (d_vastago - X_ejecentroidal_vastago) ** 2, 4)
    fss_vastago= params['fss_vastago'] = round(M_servicio_vastago * (d_vastago - X_ejecentroidal_vastago) * relacionmodular_estribo / I_vastago, 2)
    beta_s_vastago = params['beta_s_vastago'] = round(1 +(recub_vastago / (0.7 * (espesor_vastago - recub_vastago))), 2)
    separacion_maxima_agrietamiento_vastago = params['separacion_maxima_agrietamiento_vastago'] = round((123000 * gamma_e_vastago / (beta_s_vastago * fss_vastago/1000) - 2 * recub_vastago)/10, 2) 
    if separacion_maxima_agrietamiento_vastago < separacion_flexion_vastago :
        print('no cumple control de agrietamiento en el vástago')
    
  
    # Diseño de la armadura de la zapata 
    # Diseño de la zarpa delantera de la zapata
    # Mu_flexion_zarpa_delantera: Momento último de diseño de la zarpa delantera en la unión zarpa delantera con el vástago, kNm/m
    # Mu_flexion_diseño_zarpa_delantera: Momento de diseño escogido como el menor entre MCR_vastago y Mu_flexion_zarpa_delantera segun Art 5.7.3.3.2, kNm/m
    
    
    ## recub_zapata: recubrimiento de concreto de la zapata, m
    # phi_zapata: factor phi utilizado en la ecuación de la cuantía.
    # d_zapata: distancia desde la cara superior hasta el centroide del acero a tracción, m
    # cuantía_zarpa_delantera: Cuantia de acero a flexión para la zarpa delantera.
    # As_flexion_zarpa_delantera: Área de acero para flexión por m de ancho de la zarpa delantera, cm2
    # As_5: Área de una barra #5, cm2.
    # No_barras_5_flexion_zarpa_delantera: Número de barras #5 necesarias para cumplir el área de acero requerida. 
    # separacion_flexion_zarpa_delantera: Separación entre barras en la zarpa delantera para el diseño a flexión, cm
   
   
   
    Mu_flexion_zarpa_delantera = params['Mu_flexion_zarpa_delantera'] = round(esfuerzo_suelo_max_resistencia *1000 * (ancho_base - espesor_vastago) ** 2 / 2, 2)
    
    if MCR_vastago < 1.33 * Mu_flexion_zarpa_delantera :
        Mu_diseño_flexion_zarpa_delantera = MCR_vastago
    else :
        Mu_diseño_flexion_zarpa_delantera = 1.33 * Mu_flexion_zarpa_delantera

    params['Mu_diseño_flexion_zarpa_delantera'] = Mu_diseño_flexion_zarpa_delantera

    recub_zapata = params['recub_zapata'] = params.get('recub_zapata', 0.08)
    phi_zapata = params['phi_zapata'] = params.get('phi_zapata', 0.9)
    d_zapata = params['d_zapata'] = round( espesor_vastago - recub_zapata ,2)
   
    cuantia_zarpa_delantera_flexion = params['cuantia_zarpa_delantera_flexion'] = round((1-(1-(2 * Mu_diseño_flexion_zarpa_delantera / (phi_zapata * 1 * d_zapata ** 2 * 0.85 * fc_estribo *1000))) ** 0.5) * 0.85* fc_estribo / fy , 5)
    As_flexion_zarpa_delantera = params['As_flexion_zarpa_delantera'] = round(cuantia_zarpa_delantera_flexion * d_zapata *100 * 100, 2)
    As_5 = params['As_5'] = 1.99
    No_barras_5_flexion_zarpa_delantera = params['No_barras_5_flexion_zarpa_delantera'] = math.ceil(As_flexion_zarpa_delantera / As_5)
    separacion_flexion_zarpa_delantera = params['separacion_flexion_zarpa_delantera'] = round(100/ No_barras_5_flexion_zarpa_delantera)
    

    # Verificación esfuerzo cortante
    # Vu_zapata_vastago: Fuerza cortante en la unión zapta vástago por m de estribo, kN
    # beta_cortante: factor que indica la capacidad del concreto agrietado diagonalmente de transmitir tracción y cortante, Art 5.8.3.4
    # theta_cortante: ángulo inclinación fisuras, Art 5.8.3.4, grados
    # Vn_zapata_vastago: Máxima fuerza cortante nominal de acuerdo con Art. 5.8.3.3, kN
    # Vc_zapata_vastago: Máxima fuerza cortante resistida por el concreto, kN
    # phi_cortante: Factor phi de resistencia
    # Vu_cortante_concreto: fuerza cortante última resistida por el concreto, kN
    
    Vu_zapata_vastago =params['Vu_zapata_vastago'] =round((ancho_base - espesor_vastago - altura_base)* esfuerzo_suelo_max_resistencia *1000, 2)

    if 3 * d_zapata > (ancho_base - espesor_vastago):
        beta_cortante = 2 ;  theta_cortante = 45
    else :
        print('revisar cortante en zapata')
    params['beta_cortante'] = beta_cortante
    params['tetha_cortante'] = theta_cortante


    Vn_zapata_vastago = params['Vn_zapata_vastago'] = 0.25 * fc_estribo * 1 * d_zapata
    Vc_zapata_vastago = params['Vc_zapata_vastago'] = round(0.083 * beta_cortante * (fc_estribo) ** 0.5 *1 * d_zapata *1000,2) 
    phi_cortante = params['phi_cortante'] = params.get('phi_cortante', 0.9)
    Vu_cortante_concreto = params['Vu_cortante_concreto'] = phi_cortante * Vc_zapata_vastago 

    if Vu_cortante_concreto < Vu_zapata_vastago :
        print('no cumple con la fuerza cortante resistida por el concreto')
    
    # Diseño de la zarpa trasera de la zapata
    # 
    # Mu_flexion_zarpa_trasera: Momento último de diseño de la zarpa delantera en la unión zarpa trasera con el vástago, kNm/m
    # Mu_flexion_diseño_zarpa_trasera: Momento de diseño escogido como el menor entre MCR_vastago y Mu_flexion_zarpa_trasera segun Art 5.7.3.3.2, kNm/m
    
    
    # recub_zapata: recubrimiento de concreto de la zapata, m
    # phi_zapata: factor phi utilizado en la ecuación de la cuantía.
    # d_zapata: distancia desde la cara superior hasta el centroide del acero a tracción, m
    # cuantía_zarpa_trasera: Cuantia de acero a flexión para la zarpa trasera.
    # As_flexion_zarpa_trasera: Área de acero para flexión por m de ancho de la zarpa trasera, cm2
    # As_5: Área de una barra #5, cm2.
    # No_barras_flexion_zarpa_trasera: Número de barras #5 necesarias para cumplir el área de acero requerida. 
    # separacion_flexion_zarpa_trasera: Separación entre barras en la zarpa trasera para el diseño a flexión, cm
    


    Mu_flexion_zarpa_trasera = params['Mu_flexion_zarpa_trasera'] = round(factor_carga_EV_MyE_max * DC_relleno * (X_a_relleno - ancho_base) + factor_carga_DC_max * altura_base * pesoespecifico_concreto * (ancho_talon ** 2) / 2 - esfuerzo_suelo_min_resistencia*1000 * (ancho_estribo - 2*e_min_resistencia - ancho_base)**2/2, 2)
    
    if MCR_vastago < 1.33 * Mu_flexion_zarpa_trasera:
        Mu_diseño_flexion_zarpa_trasera = MCR_vastago
    else :
        Mu_diseño_flexion_zarpa_trasera = 1.33 * Mu_flexion_zarpa_trasera

    params['Mu_diseño_flexion_zarpa_trasera'] = Mu_diseño_flexion_zarpa_trasera

    cuantia_zarpa_trasera_flexion = params['cuantia_zarpa_trasera_flexion'] = round((1-(1-(2 * Mu_diseño_flexion_zarpa_trasera / (phi_zapata * 1 * d_zapata ** 2 * 0.85 * fc_estribo *1000))) ** 0.5) * 0.85* fc_estribo / fy , 5)
    As_flexion_zarpa_trasera = params['As_flexion_zarpa_trasera'] = round(cuantia_zarpa_trasera_flexion * d_zapata *100 * 100, 2)
    As_5 = params['As_5'] = 1.99
    No_barras_flexion_zarpa_trasera = params['No_barras_5_flexion_zarpa_trasera'] = math.ceil(As_flexion_zarpa_trasera / As_4)
    separacion_flexion_zarpa_trasera = params['separacion_flexion_zarpa_trasera'] = round(100/ No_barras_flexion_zarpa_trasera)
    
    # Armadura por retracción de fraguado y temperatura en la zapata

    # As_retraccionytemperatura_zapata: Área de refuerzo por retracción y temperatura, mm2, Art 5.10.8
    # As_4: Área de una barra #4, cm2
    # No_barras_4_retraccionytemperatura_zapata: Número de barras necesarias para cumplir el refuerzo minimo por retracción de fraguado y temperatura.
    # separacion_retraccionytemperatura_zapata: separación de las barras de refuerzo por retracción de fraguado y temperatura, cm  

    As_retraccionytemperatura_zapata = params['As_retraccionytemperatura_zapata'] = round(750 * ancho_estribo * altura_talon *1000 /( 2 * (ancho_estribo + altura_talon) * fy),2)
    if As_retraccionytemperatura_vastago < 234 or As_retraccionytemperatura_vastago > 1278 :
        print( 'no cumple armadura por retracción y temperatura' ) 
    As_4 = params['As_4'] = 1.29
    No_barras_4_retraccionytemperatura_zapata = params['No_barras_4_retraccionytemperatura_zapata'] = math.ceil(As_retraccionytemperatura_zapata /100 / As_4)
    separacion_retraccionytemperatura_zapata = params['separacion_retraccionytemperatura_zapata'] = round(100 / No_barras_4_retraccionytemperatura_zapata, 2)
    
   
    return params

if __name__ == '__main__':
    # diseño estribo libro profesor Carlos Vallecilla
    filename = 'test - estribo superficial.docx'
    params = {
        'PGA': 0.25,
        'numero_carriles': 2,

        'altura_estribo': 7.7,
        'ancho_estribo': 4.9,
        'largo_estribo': 7.8,
        'altura_vastago': 5.2,
        'espesor_vastago': 0.9,
        'altura_base': 0.9,
        'ancho_base': 2.1,
        'altura_talon': 0.9,
        'ancho_talon': 2.8,
        'altura_espaldar':2.1,
        'espesor_espaldar': 0.3,
        'distanciaalabase_espaldar': 4.7,
        'cantidad_topes' : 2,
        'altura_topes': 1.1,
        'largo_topes': 0.9,
        'ancho_topes' : 0.8,
        'cantidad_aletas' : 2,
        'altura_aletas' : 6.8,
        'ancho_aletas' : 2.8,
        'espesor_base_aletas' : 0.7,
        'espesor_corona_aletas': 0.3,
        'peso_losa': 42.14,
        'L_superestructura': 22,
        'cantidad_vigas': 3,
        'peso_vigas': 15.3036,
        'peso_anden' : 5.886,
        'peso_bordillo': 1.64808,
        
        'F_PGA': 1.15,
        



    }

    params = design(params)

    doc.render(params)
    doc.save(filename)