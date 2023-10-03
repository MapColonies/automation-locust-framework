import requests

body = {"positions": [{"longitude": 34.98268650480549, "latitude": 32.76615952759517}, {"longitude": 35.02584136109213, "latitude": 32.77286449047748}, {"longitude": 35.052715407259164, "latitude": 32.76596810873514}, {"longitude": 34.999360845994474, "latitude": 32.77051923124113}, {"longitude": 35.03621073857996, "latitude": 32.783175242695386}, {"longitude": 35.01345282865174, "latitude": 32.76963278130549}, {"longitude": 34.97549368826326, "latitude": 32.79078388401759}, {"longitude": 35.039185590105454, "latitude": 32.75753461233493}, {"longitude": 35.02559211574353, "latitude": 32.778963775702785}, {"longitude": 35.005805414212446, "latitude": 32.80120918984481}, {"longitude": 35.035426884771134, "latitude": 32.80265330045601}, {"longitude": 35.061392775200865, "latitude": 32.75952736977803}, {"longitude": 35.06117966538358, "latitude": 32.763057383736665}, {"longitude": 35.020248987426115, "latitude": 32.76084981019331}, {"longitude": 35.03081526913101, "latitude": 32.776318678513846}, {"longitude": 34.99396990688773, "latitude": 32.76558348191271}, {"longitude": 34.97670379650176, "latitude": 32.75824743080084}, {"longitude": 35.02403542324851, "latitude": 32.77722041421994}, {"longitude": 35.06246453756539, "latitude": 32.798313443548494}, {"longitude": 35.01593488315498, "latitude": 32.7688945514881}, {"longitude": 35.03096580811895, "latitude": 32.799907304982916}, {"longitude": 35.05224232939624, "latitude": 32.80038065935366}, {"longitude": 35.04643549978859, "latitude": 32.770468076353175}, {"longitude": 35.05856008229324, "latitude": 32.784117927758125}, {"longitude": 34.98056200160778, "latitude": 32.76710177618829}, {"longitude": 35.043196822237675, "latitude": 32.789906920122384}, {"longitude": 34.98525697754395, "latitude": 32.77327696379664}, {"longitude": 34.98027777286325, "latitude": 32.766026118907824}, {"longitude": 34.97232119754285, "latitude": 32.77066506518936}, {"longitude": 34.98399808124359, "latitude": 32.78429299003578}, {"longitude": 35.02164770086063, "latitude": 32.77445904064939}, {"longitude": 34.98896294215016, "latitude": 32.79220853464216}, {"longitude": 34.97503001032758, "latitude": 32.75907444064837}, {"longitude": 35.03779439746801, "latitude": 32.76307801923792}, {"longitude": 35.06077478875001, "latitude": 32.7579797032371}, {"longitude": 35.037220088845565, "latitude": 32.791255490954526}, {"longitude": 35.0287870591791, "latitude": 32.78995233384999}, {"longitude": 34.972334388976876, "latitude": 32.778039902019444}, {"longitude": 35.02240923837752, "latitude": 32.76883521726366}, {"longitude": 35.05052715488767, "latitude": 32.769431616330216}, {"longitude": 35.04895327141476, "latitude": 32.76227157578864}, {"longitude": 35.05511204170603, "latitude": 32.79116720207805}, {"longitude": 35.00036837890318, "latitude": 32.79123969424243}, {"longitude": 34.981097033598495, "latitude": 32.77132077941907}, {"longitude": 35.01220705661496, "latitude": 32.775760920576126}, {"longitude": 35.05744111391989, "latitude": 32.773885597789565}, {"longitude": 35.03931331207724, "latitude": 32.80039062040981}, {"longitude": 35.055963791901036, "latitude": 32.76869264088377}, {"longitude": 35.02691844524255, "latitude": 32.76787857415961}, {"longitude": 34.975886147802, "latitude": 32.796912152455235}, {"longitude": 35.003054172418935, "latitude": 32.790320495590464}, {"longitude": 35.02085325977913, "latitude": 32.77419805406013}, {"longitude": 35.03202187971905, "latitude": 32.77206337010146}, {"longitude": 35.03099005478907, "latitude": 32.800064597286905}, {"longitude": 34.996333330634414, "latitude": 32.7753276545283}, {"longitude": 35.019429664477464, "latitude": 32.76982781117665}, {"longitude": 35.06312355093532, "latitude": 32.79765358806907}, {"longitude": 35.05751245713632, "latitude": 32.77790548822363}, {"longitude": 35.03575609795753, "latitude": 32.79775138177715}, {"longitude": 35.00966388707466, "latitude": 32.80217997543456}, {"longitude": 35.05470318269922, "latitude": 32.7648988128427}, {"longitude": 35.00445004476013, "latitude": 32.80225900035618}, {"longitude": 35.029095773602215, "latitude": 32.80014884738517}, {"longitude": 35.032297892925314, "latitude": 32.78938476499954}, {"longitude": 34.98732705442928, "latitude": 32.78686366169946}, {"longitude": 35.04643276374161, "latitude": 32.78039904011702}, {"longitude": 35.00265117306304, "latitude": 32.777375498655964}, {"longitude": 34.97671648600839, "latitude": 32.80094047209244}, {"longitude": 35.02079683811094, "latitude": 32.76563669660545}, {"longitude": 35.04568141921309, "latitude": 32.76416041555106}, {"longitude": 35.06417828014353, "latitude": 32.76660555492734}, {"longitude": 34.989094327242945, "latitude": 32.769411771604915}, {"longitude": 35.0493630420719, "latitude": 32.77927089288904}, {"longitude": 35.000433971618634, "latitude": 32.766632600480435}, {"longitude": 35.02962783229275, "latitude": 32.79950810241907}, {"longitude": 34.992349756251066, "latitude": 32.79599458427797}, {"longitude": 35.01301339875304, "latitude": 32.77203852562714}, {"longitude": 35.01517346538067, "latitude": 32.78642290673571}, {"longitude": 35.05182616816908, "latitude": 32.76337972661692}, {"longitude": 35.05168483997061, "latitude": 32.7951132721893}, {"longitude": 34.990400856066735, "latitude": 32.796991302215346}, {"longitude": 34.98374714382068, "latitude": 32.782374545787384}, {"longitude": 35.04627019480194, "latitude": 32.76747239623591}, {"longitude": 34.98968183446122, "latitude": 32.782680055503484}, {"longitude": 35.02911871571362, "latitude": 32.77619396653872}, {"longitude": 35.00727827677412, "latitude": 32.80088432899441}, {"longitude": 34.990819501905825, "latitude": 32.77256839614337}, {"longitude": 35.03837547292613, "latitude": 32.7618745261136}, {"longitude": 35.058077491951636, "latitude": 32.791225065533865}, {"longitude": 35.01345920465543, "latitude": 32.802348760421786}, {"longitude": 35.012989798489706, "latitude": 32.800874139827094}, {"longitude": 35.02089026158258, "latitude": 32.785814631605625}, {"longitude": 35.061176458794954, "latitude": 32.804088927169495}, {"longitude": 35.02209412235997, "latitude": 32.766457325417306}, {"longitude": 34.97260244868159, "latitude": 32.803216957422336}, {"longitude": 35.05895698050082, "latitude": 32.77628829534388}, {"longitude": 34.98534646137803, "latitude": 32.7653094051567}, {"longitude": 34.99687887948116, "latitude": 32.794202945569026}, {"longitude": 35.059723682666366, "latitude": 32.78086855325464}, {"longitude": 35.00728065545234, "latitude": 32.773102697217176}, {"longitude": 34.972629530212025, "latitude": 32.7736319124426}, {"longitude": 35.0188744680692, "latitude": 32.78770718454852}, {"longitude": 34.999429311582716, "latitude": 32.768858056498956}, {"longitude": 34.98380079936291, "latitude": 32.79585020222702}, {"longitude": 34.97522307764054, "latitude": 32.78957260295213}, {"longitude": 34.985883920508954, "latitude": 32.800437470650444}, {"longitude": 34.979401325207654, "latitude": 32.76879874795416}, {"longitude": 35.05038577827869, "latitude": 32.79618671843285}, {"longitude": 34.999100279742756, "latitude": 32.7590660073599}, {"longitude": 35.021285189941295, "latitude": 32.77273229331644}, {"longitude": 34.980083989094005, "latitude": 32.77861945110749}, {"longitude": 35.060059756071446, "latitude": 32.792585391883186}, {"longitude": 34.98688407100233, "latitude": 32.77073262891039}, {"longitude": 34.97685795657126, "latitude": 32.78820250348867}, {"longitude": 35.04639859753145, "latitude": 32.77796453295785}, {"longitude": 35.009725967396946, "latitude": 32.776540012005796}, {"longitude": 35.02035736054044, "latitude": 32.78293279148192}, {"longitude": 34.98130417595879, "latitude": 32.77431451091584}, {"longitude": 34.973117064316, "latitude": 32.775758819416026}, {"longitude": 35.0359928604694, "latitude": 32.78129365104465}, {"longitude": 35.04639740852175, "latitude": 32.78555993514152}, {"longitude": 35.03688843568447, "latitude": 32.78790765467271}, {"longitude": 35.0138900036635, "latitude": 32.801457412278246}, {"longitude": 34.98385574606447, "latitude": 32.78952573917811}, {"longitude": 34.97222471154633, "latitude": 32.77149381526141}, {"longitude": 34.98335884122533, "latitude": 32.79560504483422}, {"longitude": 34.98155539559604, "latitude": 32.78226373423804}, {"longitude": 35.043426231256014, "latitude": 32.79736466505561}, {"longitude": 34.97357073585531, "latitude": 32.787189217210894}, {"longitude": 34.98501423584863, "latitude": 32.8023819634255}, {"longitude": 35.04218415172586, "latitude": 32.762841059706886}, {"longitude": 34.98022217526825, "latitude": 32.77926841132276}, {"longitude": 35.04313687083117, "latitude": 32.78854983672513}, {"longitude": 35.039546241418336, "latitude": 32.76701696558306}, {"longitude": 35.04891876558791, "latitude": 32.77072994558082}, {"longitude": 35.01376284583124, "latitude": 32.769853808161805}, {"longitude": 34.99499867547468, "latitude": 32.79397511119726}, {"longitude": 34.995670859265786, "latitude": 32.77259564214773}, {"longitude": 35.03218438966669, "latitude": 32.756748149664254}, {"longitude": 34.98868755142642, "latitude": 32.7618017480964}, {"longitude": 35.007436317463934, "latitude": 32.78488086083869}, {"longitude": 35.029512400767985, "latitude": 32.77198875528662}, {"longitude": 35.05931184406888, "latitude": 32.76329371149446}, {"longitude": 35.01424741685297, "latitude": 32.76703173640489}, {"longitude": 35.056074953795104, "latitude": 32.78060950605338}, {"longitude": 35.004267109728104, "latitude": 32.797312634526754}, {"longitude": 35.05410663215961, "latitude": 32.75985358269831}, {"longitude": 34.99515122685952, "latitude": 32.780603487510085}, {"longitude": 35.01554750014227, "latitude": 32.76042019026736}, {"longitude": 35.003646986177635, "latitude": 32.77913635280908}, {"longitude": 35.038893733559405, "latitude": 32.781299344166975}, {"longitude": 35.00860898907327, "latitude": 32.77147939822035}, {"longitude": 35.03432830977396, "latitude": 32.757695037354075}, {"longitude": 35.0550936373045, "latitude": 32.76113207079241}, {"longitude": 35.060101949529034, "latitude": 32.78582213828042}, {"longitude": 34.98639498200613, "latitude": 32.78361405701572}, {"longitude": 35.0390538568193, "latitude": 32.79817739955604}, {"longitude": 35.06025646611716, "latitude": 32.757703198614855}, {"longitude": 34.99247457251642, "latitude": 32.801477087522805}, {"longitude": 34.98367460986503, "latitude": 32.77193505353704}, {"longitude": 35.0521840969551, "latitude": 32.791817585862326}, {"longitude": 35.0589280487346, "latitude": 32.80342584036512}, {"longitude": 35.01421770931918, "latitude": 32.759781681779785}, {"longitude": 35.005476842127415, "latitude": 32.76197900832535}, {"longitude": 35.03800442863243, "latitude": 32.79207778575613}, {"longitude": 34.9956125069057, "latitude": 32.78289078933}, {"longitude": 34.998852383634826, "latitude": 32.763880354411164}, {"longitude": 35.01454470228332, "latitude": 32.760905540135056}, {"longitude": 35.029810848155215, "latitude": 32.766313034113736}, {"longitude": 34.98657282830542, "latitude": 32.76458464336678}, {"longitude": 35.05596764249896, "latitude": 32.79542566200067}, {"longitude": 35.04592305483037, "latitude": 32.765413367786785}, {"longitude": 34.97197448261939, "latitude": 32.765406726053165}, {"longitude": 35.052228477515214, "latitude": 32.77154334089867}, {"longitude": 35.02462419898811, "latitude": 32.79070662526467}, {"longitude": 35.009131810447705, "latitude": 32.75626818488795}, {"longitude": 35.015150829412214, "latitude": 32.76615579092404}, {"longitude": 35.013001469888934, "latitude": 32.79319112768598}, {"longitude": 35.03930907411996, "latitude": 32.78350480365338}, {"longitude": 35.058543652104234, "latitude": 32.7759937311119}, {"longitude": 35.01624235089186, "latitude": 32.78396416099037}, {"longitude": 35.04573462492992, "latitude": 32.78158908158834}, {"longitude": 35.0380190322936, "latitude": 32.75910113425736}, {"longitude": 35.06414746046826, "latitude": 32.76896725805003}, {"longitude": 35.03561783881856, "latitude": 32.764850203583116}, {"longitude": 35.05147098769252, "latitude": 32.765417588589465}, {"longitude": 34.9899879805722, "latitude": 32.76276613364322}, {"longitude": 35.023415476710845, "latitude": 32.788117990606715}, {"longitude": 34.980309594663666, "latitude": 32.764804472310985}, {"longitude": 35.045671822524376, "latitude": 32.76931524021041}, {"longitude": 35.053126783892175, "latitude": 32.78689377190421}, {"longitude": 35.00188727565603, "latitude": 32.76825127810428}, {"longitude": 35.00691706880002, "latitude": 32.77180353228583}, {"longitude": 35.03733553703481, "latitude": 32.79459883845058}, {"longitude": 35.01875784473384, "latitude": 32.800576714477685}, {"longitude": 35.060935084458876, "latitude": 32.764283230632635}, {"longitude": 35.02360378001468, "latitude": 32.79338483023016}, {"longitude": 35.01084364657154, "latitude": 32.78701848742999}, {"longitude": 35.03150861356399, "latitude": 32.75798421539745}, {"longitude": 35.0144734814803, "latitude": 32.78753332452325}, {"longitude": 34.9993896174903, "latitude": 32.78714202340703}, {"longitude": 35.01204708447764, "latitude": 32.80032691910745}, {"longitude": 35.006430126049366, "latitude": 32.795802896236395}, {"longitude": 35.054569405867916, "latitude": 32.76852280038271}, {"longitude": 35.022259602470704, "latitude": 32.79553185856135}, {"longitude": 35.01691498259938, "latitude": 32.7591066346526}, {"longitude": 34.99385564105297, "latitude": 32.79163611713011}, {"longitude": 35.045914398735114, "latitude": 32.770369265496655}, {"longitude": 35.00705421138148, "latitude": 32.78306561412692}, {"longitude": 35.01279121785202, "latitude": 32.76319071272495}, {"longitude": 34.99729123676029, "latitude": 32.79437747891007}, {"longitude": 35.01144441669793, "latitude": 32.76274291011}, {"longitude": 35.0125384029691, "latitude": 32.794097414627934}, {"longitude": 35.041106752668355, "latitude": 32.802517293937406}, {"longitude": 35.02733330714852, "latitude": 32.77873237016037}, {"longitude": 34.99301576010446, "latitude": 32.78815941746036}, {"longitude": 34.98483357840674, "latitude": 32.788362060777125}, {"longitude": 34.980502197418296, "latitude": 32.77415526149434}, {"longitude": 35.01495991394326, "latitude": 32.79918604666248}, {"longitude": 34.97189992552049, "latitude": 32.79197600176355}, {"longitude": 35.030673208027835, "latitude": 32.77685365623938}, {"longitude": 35.04833060443961, "latitude": 32.76877255878009}, {"longitude": 35.00566934387215, "latitude": 32.78255489769384}, {"longitude": 35.064819298954966, "latitude": 32.787831762282}, {"longitude": 35.03152447843429, "latitude": 32.78093441048078}, {"longitude": 35.03761634393632, "latitude": 32.783544170747014}, {"longitude": 35.00014652169898, "latitude": 32.77473180457382}, {"longitude": 35.014846557070705, "latitude": 32.797607837684666}, {"longitude": 35.057410479722435, "latitude": 32.76490848781418}, {"longitude": 35.055604969468, "latitude": 32.765176340867946}, {"longitude": 35.005655615041285, "latitude": 32.8023325137872}, {"longitude": 35.02641710385604, "latitude": 32.79683955631165}, {"longitude": 35.04702662105677, "latitude": 32.801629923629235}, {"longitude": 35.009617226105966, "latitude": 32.80267829414854}, {"longitude": 34.999334113720096, "latitude": 32.775610492714726}, {"longitude": 35.00632110984478, "latitude": 32.80290752500966}, {"longitude": 35.008640386194394, "latitude": 32.796779719414936}, {"longitude": 35.01348981208546, "latitude": 32.79191545234182}, {"longitude": 35.05863071591012, "latitude": 32.80147825268861}, {"longitude": 35.062909072768484, "latitude": 32.77673458572673}, {"longitude": 34.98045979202032, "latitude": 32.77437322947716}, {"longitude": 35.029030338405164, "latitude": 32.76119828666464}, {"longitude": 34.984599728834176, "latitude": 32.78204540580518}, {"longitude": 34.975684739778785, "latitude": 32.79466903803124}, {"longitude": 34.99342652345188, "latitude": 32.80094470125346}, {"longitude": 34.977264377229474, "latitude": 32.80255204802511}, {"longitude": 35.03907191399541, "latitude": 32.75739287274227}, {"longitude": 35.01715705715658, "latitude": 32.78136598362926}, {"longitude": 35.04663724140098, "latitude": 32.7837798246405}, {"longitude": 34.984799445862414, "latitude": 32.76868403034087}], "productType": "MIXED", "excludeFields": []}

res = requests.post(json=body, headers={"Content-Type": "application/json"},
                    url="https://dem-int-heights-production-nginx-route-integration.apps.j1lk3njp.eastus.aroapp.io/api/heights/v1/points?token=eyJhbGciOiJSUzI1NiIsImtpZCI6Im1hcC1jb2xvbmllcy1pbnQifQ.eyJkIjpbInJhc3RlciIsInJhc3RlcldtcyIsInJhc3RlckV4cG9ydCIsImRlbSIsInZlY3RvciIsIjNkIl0sImlhdCI6MTY3NDYzMjM0Niwic3ViIjoibWFwY29sb25pZXMtYXBwIiwiaXNzIjoibWFwY29sb25pZXMtdG9rZW4tY2xpIn0.D1u28gFlxf_Z1bzIiRHZonUgrdWwhZy8DtmQj15cIzaABRUrGV2n_OJlgWTuNfrao0SbUZb_s0_qUUW6Gz_zO3ET2bVx5xQjBu0CaIWdmUPDjEYr6tw-eZx8EjFFIyq3rs-Fo0daVY9cX1B2aGW_GeJir1oMnJUURhABYRoh60azzl_utee9UdhDpnr_QElNtzJZIKogngsxCWp7tI7wkTuNCBaQM7aLEcymk0ktxlWEAt1E0nGt1R-bx-HnPeeQyZlxx4UQ1nuYTijpz7N8poaCCExOFeafj9T7megv2BzTrKWgfM1eai8srSgNa3I5wKuW0EyYnGZxdbJe8aseZg")

print(type(res.json()))
points_data = res.json()["data"]
null_heights = []
for height in points_data:
    if height["height"] is None:
        null_heights.append(height)
print(null_heights)

def parse_response_content(
        response_content: dict,
        response_time: float,
        normality_threshold: dict,
        property_name: str,
):
    """
    This function will parse elevation response by content values
    :param response_content: locust user response content
    :param  response_time: response time of users requests
    :param normality_threshold: response time dict with fast response time and slow response time
    :param property_name: the property name to be extracted from response content
    :return:
    if invalid return the request value
    """
    unusual_results = {}
    if (
            response_time <= normality_threshold["low_response_time"]
            or response_time >= normality_threshold["high_response_time"]
    ):
        unusual_results["anomaly_response_time"] = response_time
        unusual_results["response_body"] = [response_content]
    null_points = [
        item for item in response_content["data"] if item.get(property_name) is None
    ]
    if null_points:
        unusual_results["anomaly_response_time"] = response_time
        unusual_results["response_body"] = null_points

    return unusual_results