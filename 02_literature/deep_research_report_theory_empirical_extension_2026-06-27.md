# Literature Master - Thesis Extension

## Propósito y contexto del proyecto

Este documento sustituye y amplía el `literature_master.md` orientado a trabajo final de curso. Su función es operar como **documento de control del corpus** para la propuesta de tesis y para la tesis posterior: decide qué fuentes deben entrar, qué función cumple cada una, qué afirmaciones pueden sostener con seguridad, dónde encajan en la propuesta y qué vacíos siguen abiertos. En esta sesión no pude inspeccionar directamente los archivos del repositorio citados en el prompt, así que la auditoría se basa en la lista de claves, el diseño empírico y la arquitectura conceptual facilitadas por ti.

| Campo | Valor |
|---|---|
| Título | *When Do Critical-Mineral Export Controls Bind? China's Licensing-Based Controls and Heterogeneous Trade Responses* |
| Pregunta de investigación | ¿Por qué controles chinos de licencias de exportación formalmente similares generan disrupciones comerciales y de precios distintas entre minerales críticos? |
| Tipo de proyecto | Propuesta de tesis de máster, ampliable a tesis completa |
| Campo | Economía china; comercio internacional; economía empírica; economía política internacional; economic statecraft |
| Diseño empírico central | Panel mensual importador × producto × fuente × mes con UN Comtrade; PPML de triple diferencia sobre cuota/fuente; diagnósticos staggered/event-study; análisis de cuñas de precios |

**Diagnóstico general**. La base actual ya cubre bien la **cronología institucional china** y la **identificación básica con PPML/DiD**, pero todavía necesita tres refuerzos decisivos: una teoría explícita de la **licencia como cuña administrativa** distinta de una prohibición; una teoría de **heterogeneidad de binding** basada en concentración, coproductos, sustitución e inventarios; y un bloque metodológico más fuerte sobre **DDD**, **staggered DiD en contextos gravity/trade** y **inferencia con pocos shocks independientes**. La literatura nueva propuesta abajo cubre exactamente esos tres huecos. citeturn14search0turn34view0turn35view0turn18search4turn18search1turn25search1turn31search0turn32search0turn28search0

## Reglas del corpus y auditoría del corpus existente

### Reglas del corpus

La regla de admisión debe ser estricta. En la propuesta de tesis, una fuente entra en el corpus activo solo si hace al menos una de estas funciones con nombre propio: precisar el mecanismo de licencias, sustentar un moderador de heterogeneidad, justificar un estimador concreto, resolver un problema de inferencia concreto, o aportar detalle institucional/producto sin el cual no puede codificarse tratamiento, timing o alcance. La clasificación operativa debe ser:

- **must-cite**: indispensable para la lógica del argumento o del método.
- **should-cite**: muy probable en propuesta/tesis, pero no estructuralmente indispensable.
- **optional**: útil para un punto estrecho, un apéndice o una objeción probable.
- **deferred**: relevante, pero no entra en el corpus activo hasta que el recorte temporal o el capítulo concreto lo exijan.

Además, conviene separar de forma explícita tres capas: **literatura académica**, **documentos oficiales/institucionales** y **fuentes de mercado/producto**. La tesis no debe presentar fuentes oficiales como si fueran teoría, ni teoría como si codificara treatment timing. La literatura nueva sobre NTMs, licencias y costes de tiempo deja claro que un requisito de licencia es una **medida administrativa distinta** de una prohibición o de una cuota y que su efecto económico depende de opacidad, demora, documentación y discrecionalidad, no solo del texto legal. citeturn14search0turn34view0turn35view0turn4search3turn5search1turn5search3

### Auditoría del corpus existente

| Citation key | Clasificación | Decisión operativa | Motivo breve |
|---|---|---|---|
| `farrell2019weaponized` | keep as must-cite | Mantener | Marco base de chokepoints y poder de red |
| `farrell2023underground_empire` | keep as should-cite | Mantener | Actualiza el marco geoeconómico, pero no sustituye al artículo de 2019 |
| `egger2024sanctions` | keep as should-cite | Mantener | Útil para ubicar coerción/economic statecraft; demasiado amplio para mecanismo de licencias |
| `bown2020semiconductor` | keep as optional | Mantener | Contexto geopolítico útil, no central para identificación |
| `bown2024semiconductors` | keep as should-cite | Mantener | Mejor pieza contextual para rivalidad tecnológica y escalada de controles |
| `bis_2022_oct7_semiconductor_controls` | keep as optional | Mantener | Cronología primaria contextual |
| `bis_2024_dec2_semiconductor_controls` | keep as should-cite | Mantener | Relevante para contextualizar retaliación mineral china posterior |
| `prc_2020_export_control_law` | keep as must-cite | Mantener | Base legal obligatoria del régimen |
| `scio_2021_chinas_export_controls` | keep as should-cite | Mantener | Síntesis oficial del sistema; complemento, no sustituto, de la ley |
| `mofcom_2006_graphite_temporary_controls` | keep as optional | Mantener | Solo para antecedente histórico o nota de continuidad institucional |
| `mofcom_2023_gallium_germanium_controls` | keep as must-cite | Mantener | Inicio de tratamiento central |
| `mofcom_2023_gallium_germanium_approvals` | keep as should-cite | Mantener | Evidencia clave contra la lectura “ban automático” |
| `mofcom_2023_gallium_germanium_license_guide` | keep as must-cite | Mantener | Mecanismo operativo de documentación/licencia |
| `mofcom_2023_graphite_controls` | keep as must-cite | Mantener | Inicio de tratamiento central |
| `mofcom_2023_graphite_license_guide` | keep as must-cite | Mantener | Mecanismo operativo de documentación/licencia |
| `mofcom_2024_graphite_faq` | keep as should-cite | Mantener | Aclara alcance y reduce error de clasificación HS |
| `mofcom_2024_graphite_approvals` | keep as should-cite | Mantener | Nuevamente útil para separar licencia de prohibición |
| `mofcom_2024_antimony_controls` | keep as must-cite | Mantener | Inicio de tratamiento central |
| `mofcom_2024_antimony_license_review` | keep as should-cite | Mantener | Evidencia institucional de revisión/licencia en curso |
| `mofcom_2024_us_controls_critical_minerals` | keep as optional | Mantener con advertencia | Contexto posterior; no mezclar con muestra principal salvo periodización separada |
| `mofcom_2025_w_te_bi_mo_in_controls` | demote/defer | Diferir | Solo entra si la ventana muestral se amplía a 2025 |
| `mofcom_2025_medium_heavy_rare_earth_controls` | demote/defer | Diferir | Igual que arriba; útil para extensión, no para propuesta base |
| `mofcom_2025_suspend_us_controls_art2` | demote/defer | Diferir | Útil para limpieza de muestra 2025, no para corpus activo base |
| `mofcom_2025_suspend_55_58_61_62` | demote/defer | Diferir | Igual que arriba |
| `usgs_2026_gallium` | keep as must-cite | Mantener | Estructura de mercado y usos |
| `usgs_2026_germanium` | keep as must-cite | Mantener | Estructura de mercado y usos |
| `usgs_2026_graphite_natural` | keep as must-cite | Mantener | Estructura de mercado y usos |
| `usgs_2026_antimony` | keep as must-cite | Mantener | Estructura de mercado y usos |
| `iea_2025_global_critical_minerals_outlook` | keep as must-cite | Mantener | Concentración, diversificación y exposición estratégica |
| `frenzel2017byproduct_metals` | keep as must-cite | Mantener | Núcleo teórico para gallio/germanio/indio como coproductos |
| `park2025graphite_supply_chain` | keep as optional | Mantener con verificación | Puede ser útil, pero hay que verificar estado editorial |
| `vandenbrink2022antimony_resilience` | keep as optional | Mantener con verificación | Útil como backup sectorial |
| `xu2025antimony_material_flow` | keep as optional | Mantener con verificación | Más útil para contexto de demanda que para mecanismo de binding |
| `santossilva2006gravity` | keep as must-cite | Mantener | Base PPML imprescindible |
| `callaway2021difference` | keep as must-cite | Mantener | Staggered DiD moderno imprescindible |
| `sun2021eventstudies` | keep as must-cite | Mantener | Event-study con heterogeneidad |
| `dechaisemartin2020twfe` | keep as should-cite | Mantener | Problemas TWFE; verificar versión exacta citada |
| `rambachan2023honest` | keep as should-cite | Mantener | Sensibilidad a pretrends |
| `roth2022pretest` | citation-key cleanup needed | Mantener pero limpiar | Conviene mapear al artículo publicado de Roth et al. 2023 si la clave aún refleja working paper |

**Limpieza de claves prioritaria**. Las claves que más probablemente necesiten ajuste bibliográfico son `roth2022pretest` y, dependiendo de cómo esté hoy el `.bib`, `dechaisemartin2020twfe`. También deben verificarse `park2025graphite_supply_chain`, `vandenbrink2022antimony_resilience` y `xu2025antimony_material_flow` antes de tratarlas como literatura académica central.

## Estructura por corrientes literarias

La estructura óptima son **siete corrientes**. No deben mezclarse, porque responden a preguntas distintas.

**Economic statecraft y export controls**. Esta corriente sirve para justificar por qué el caso importa y por qué los minerales críticos son un instrumento plausible de poder estructural. Aquí el artículo de Farrell y Newman es el ancla, mientras que la literatura reciente sobre restricciones a materias primas muestra que los controles de exportación han crecido con rapidez en el contexto de seguridad económica. La afirmación segura aquí no es “China coacciona con éxito”, sino “los chokepoints y la concentración convierten restricciones formales en shocks plausibles de oferta y reasignación”. citeturn37view0turn37view2turn14search1turn10search4turn12search8turn23search9

**Instituciones chinas de control de exportaciones y episodios de política mineral**. Esta corriente sirve para codificar tratamiento, fecha efectiva, alcance material y mecanismo administrativo. La ley china de 2020, el white paper de 2021 y las guías/licence guides de MOFCOM son la base primaria. Lo decisivo es que la regulación china reciente de dual-use subraya gestión de licencias, listas de control y supervisión, mientras que la evidencia oficial de aprobaciones para solicitudes conformes impide modelar estos episodios como prohibiciones automáticas. Las afirmaciones seguras aquí son institucionales: qué exige el régimen, qué documentos pide, qué productos abarca y qué forma legal adopta. citeturn35view0turn17search9turn34view0

**Cadenas de suministro de minerales críticos y heterogeneidad de producto**. Esta corriente sirve para explicar por qué gallio, germanio, grafito y antimonio no deberían reaccionar igual. La IEA documenta alta concentración en refino/procesamiento de minerales estratégicos; la OCDE muestra una exposición alta de grafito, tierras raras y otros minerales a restricciones; USGS y Frenzel ayudan a traducir eso a estructura material concreta. Nassar y Graedel añaden la pieza clave: muchos metales críticos son coproductos con oferta menos elástica, alta concentración y sustitutibilidad limitada. La afirmación segura es que la heterogeneidad observada puede surgir de estructura de mercado y producción, no solo de intenciones políticas distintas. citeturn37view1turn37view2turn11search1turn21search1turn21search9turn12search8

**Teoría de la cuña de licencias y mecanismos de ajuste**. Esta es la corriente que más faltaba. UNCTAD clasifica por separado **prohibiciones de exportación**, **cuotas de exportación** y **requisitos de licencia para exportar**; el working paper de la OMC muestra que las licencias son procedimientos administrativos que pueden generar efectos restrictivos adicionales si son opacos o gravosos. Djankov y Hummels muestran que el tiempo y la demora administrativa son costes comerciales reales; Handley y Limão muestran que la incertidumbre de política comercial reduce entrada y comercio; Grossman, Helpman y Redding, y Handley, Kamal y Monarch, muestran que ante shocks comerciales los compradores renegocian, buscan reemplazos o cortan compras dependiendo de costes de búsqueda y disponibilidad de proveedores alternativos. Esta corriente permite formalizar tu variable latente: **cuña de licencias = riesgo de demora/denegación + coste de cumplimiento + incertidumbre + menor disponibilidad efectiva desde China**. citeturn14search0turn34view0turn4search3turn5search1turn5search3turn18search1turn18search4

**Estrategia empírica de trade flows**. Aquí la corriente debe ser mucho más estrecha que en el corpus actual. Santos Silva y Tenreyro y Fally siguen siendo indispensables para PPML/gravity con muchos ceros y FE; pero ahora hay que sumar literatura sobre DDD y gravity/staggered adoption. Olden y Møen formalizan el estimador triple diferencia y dejan claro que su interpretación causal depende de una sola condición de tendencias paralelas “en razón”, no de dos supuestos DiD independientes. Además, el trabajo reciente sobre staggered DiD en contextos gravity muestra que la combinación entre gravedad estructural y adopción escalonada es tratable, pero exige estimadores e interpretación más cuidadosos que el TWFE estándar. citeturn3search5turn38search1turn25search1turn38search12

**Inferencia staggered/event-study y problema de pocos shocks independientes**. Tu restricción de inferencia es correcta y necesita soporte explícito. Conley y Taber, Ferman y Pinto, y MacKinnon y Webb muestran que cuando la identificación descansa en un número pequeño de cambios de política, la inferencia convencional puede fallar aunque haya muchas observaciones. Borusyak, Jaravel y Spiess, junto con Callaway y Sun-Abraham, fortalecen la parte de event-study bajo staggered timing. La afirmación segura aquí es que el clustering por importador puede seguir siendo un diagnóstico útil, pero no resuelve por sí solo el problema de que las verdaderas innovaciones de política estén a nivel producto-tiempo y sean pocas. citeturn31search0turn32search0turn26search19turn28search0turn19search0

**Cuñas de precios y segmentación de mercado**. Esta corriente debe entrar, pero con rango probatorio limitado. Martin y Anderson, y la OCDE sobre restricciones a materias primas, muestran que las restricciones de exportación pueden abrir brechas entre precio doméstico e internacional y trasladar presión al exterior. El trabajo sobre volatilidad muestra además que el anuncio mismo puede mover precios, sobre todo con stocks bajos. Pero la interpretación causal debe ser prudente: cualquier comparación doméstico–internacional exige armonizar unidad, grado, localización, divisa e incoterm. Las series del IMF PCPS y del Pink Sheet del Banco Mundial son recordatorios metodológicos de que los benchmarks de commodities están definidos precisamente por esos atributos. Por tanto, en esta tesis el bloque de precios debe tratarse principalmente como **evidencia de mecanismo y corroboración**, no como único pilar causal. citeturn20search15turn20search1turn20search17turn33search0turn33search1

## Tabla canónica de fuentes y candidatos nuevos

La tabla siguiente recoge el **corpus activo recomendado** para la propuesta. Incluye fuentes existentes y fuentes nuevas admitidas por función.

| Citation Key | Full Citation | Source Type | Priority | Stream | Role in Thesis | Can Safely Support | Cannot Support | DOI / URL | Repository Status | Action |
|---|---|---|---|---|---|---|---|---|---|---|
| `farrell2019weaponized` | Farrell, H., & Newman, A. (2019), “Weaponized Interdependence” | Journal article | must-cite | Statecraft | Marco de chokepoints | Redes y coerción estructural | No identifica binding mineral específico | local/existing | Existing | Keep |
| `prc_2020_export_control_law` | PRC Export Control Law (2020) | Official legal text | must-cite | China institutions | Base legal | Naturaleza legal del régimen | No mide efectos de mercado | local/existing | Existing | Keep |
| `scio_2021_chinas_export_controls` | SCIO, *China’s Export Controls* (2021) | Official white paper | should-cite | China institutions | Visión oficial del sistema | Objetivos declarados y arquitectura | No prueba binding | local/existing | Existing | Keep |
| `mofcom_2023_gallium_germanium_controls` | MOFCOM notice on gallium/germanium controls (2023) | Official notice | must-cite | China institutions | Treatment start | Fecha y alcance jurídico | No prueba caída comercial | local/existing | Existing | Keep |
| `mofcom_2023_gallium_germanium_license_guide` | MOFCOM licence guide for gallium/germanium (2023) | Official guidance | must-cite | China institutions | Mecanismo operativo | Documentación exigida/licensing process | No observa tasas de aprobación | local/existing | Existing | Keep |
| `mofcom_2023_graphite_controls` | MOFCOM notice on graphite controls (2023) | Official notice | must-cite | China institutions | Treatment start | Fecha y alcance jurídico | No prueba binding | local/existing | Existing | Keep |
| `mofcom_2023_graphite_license_guide` | MOFCOM licence guide for graphite (2023) | Official guidance | must-cite | China institutions | Mecanismo operativo | Documentación/licencia | No mide efectos | local/existing | Existing | Keep |
| `mofcom_2024_graphite_faq` | MOFCOM graphite FAQ (2024) | Official FAQ | should-cite | China institutions | Limpieza de alcance | Clarificación de scope | No identifica impacto | local/existing | Existing | Keep |
| `mofcom_2024_antimony_controls` | MOFCOM notice on antimony controls (2024) | Official notice | must-cite | China institutions | Treatment start | Fecha y alcance jurídico | No prueba binding | local/existing | Existing | Keep |
| `usgs_2026_gallium` | USGS, *Mineral Commodity Summaries: Gallium* (2026) | Official report | must-cite | Product heterogeneity | Estructura de mercado | Usos, oferta, posición china | No identifica cuña de licencia | local/existing | Existing | Keep |
| `usgs_2026_germanium` | USGS, *Mineral Commodity Summaries: Germanium* (2026) | Official report | must-cite | Product heterogeneity | Estructura de mercado | Usos, oferta, posición china | Igual | local/existing | Existing | Keep |
| `usgs_2026_graphite_natural` | USGS, *Mineral Commodity Summaries: Natural Graphite* (2026) | Official report | must-cite | Product heterogeneity | Estructura de mercado | Usos, oferta, posición china | Igual | local/existing | Existing | Keep |
| `usgs_2026_antimony` | USGS, *Mineral Commodity Summaries: Antimony* (2026) | Official report | must-cite | Product heterogeneity | Estructura de mercado | Usos, oferta, posición china | Igual | local/existing | Existing | Keep |
| `iea_2025_global_critical_minerals_outlook` | IEA, *Global Critical Minerals Outlook 2025* | Official report | must-cite | Product heterogeneity | Concentración/diversificación | Concentración en refino y vulnerabilidad | No identifica episodios concretos | local/existing | Existing | Keep |
| `frenzel2017byproduct_metals` | Frenzel et al. (2017), “Quantifying the relative availability of high-tech by-product metals” | Journal article | must-cite | Product heterogeneity | Coproductos | Oferta derivada de host metals | No mide política china | 10.1016/j.resourpol.2017.04.008 | Existing | Keep |
| `santossilva2006gravity` | Santos Silva & Tenreyro (2006), “The Log of Gravity” | Journal article | must-cite | Trade methods | Base PPML | PPML con ceros/heterocedasticidad | No resuelve staggered timing | local/existing | Existing | Keep |
| `callaway2021difference` | Callaway & Sant’Anna (2021), “Difference-in-Differences with Multiple Time Periods” | Journal article | must-cite | Staggered inference | ATT staggered | Estimación por cohortes/tiempo | No formaliza DDD | local/existing | Existing | Keep |
| `sun2021eventstudies` | Sun & Abraham (2021), “Estimating Dynamic Treatment Effects…” | Journal article | must-cite | Staggered inference | Event-study | Diagnóstico dinámico con heterogeneidad | No resuelve pocos shocks | local/existing | Existing | Keep |
| `rambachan2023honest` | Rambachan & Roth (2023), *HonestDiD* article | Journal article | should-cite | Staggered inference | Sensibilidad a pretrends | Robustez a desvíos de tendencias paralelas | No identifica tratamiento | local/existing | Existing | Keep |
| `roth2022pretest` | Roth et al. published article/version to verify | Journal article | should-cite | Staggered inference | Advertencia sobre pretests | Riesgos de sobreconfiar en pretrends | No sustituye estimación principal | cleanup needed | Existing | Keep + clean key |
| `unctad_2019_ntm_classification` | UNCTAD (2019), *International Classification of Non-Tariff Measures* | Official classification | must-cite | Licensing wedge | Tipología de medida | Distinguir licencia, prohibición y cuota | No mide efectos económicos | stable UNCTAD page | New | Add |
| `gamberale_tarasenko_2023_export_licensing` | Gamberale, C., & Tarasenko, I. (2023), *Export Licensing in the WTO Context* | WTO working paper | must-cite | Licensing wedge | Mecanismo administrativo | Licencias como procedimiento con posible efecto restrictivo adicional | No estima shocks minerales | WTO ERSD202306 | New | Add |
| `prc_2024_dual_use_regulations` | State Council/Gov.cn (2024), regulations on export control of dual-use items | Official regulation/news release | should-cite | China institutions | Actualización operativa | Gestión de licencias, lista de control, supervisión | No mide aprobación/denegación | Gov.cn official page | New | Add |
| `bogdanova_wang_2023_china_export_restrictions_wto` | Bogdanova, I., & Wang, A. (2023), “China’s Use of Export Restrictions and WTO Law” | Book chapter | should-cite | Statecraft/China | Periodización histórica | Giro hacia uso geopolítico de restricciones | No identifica binding episodio por episodio | 10.1017/9781009291804.011 | New | Add |
| `oecd_2026_crm_export_restrictions` | OECD (2026), *Inventory of Export Restrictions on Critical Raw Materials 2026* | Official report | must-cite | Statecraft/Product | Tendencias globales y tipos de medidas | Aumento quinquenal, incidencia por mineral, tipos de restricciones | No prueba el caso chino aislado | 10.1787/d5ca8f62-en | New | Add |
| `djankov_freund_pham_2010_trading_on_time` | Djankov, Freund & Pham (2010), “Trading on Time” | Journal article | must-cite | Licensing wedge | Costes de demora | Tiempo administrativo como coste comercial | No modela licencias dual-use | doi needs verification | New | Add |
| `hummels_schaur_2013_time_trade_barrier` | Hummels & Schaur (2013), “Time as a Trade Barrier” | Journal article | must-cite | Licensing wedge | Coste del tiempo | Demora como barrera económica | No distingue motivos de demora | publisher page / DOI verify | New | Add |
| `handley_limao_2017_policy_uncertainty` | Handley & Limão (2017), “Policy Uncertainty, Trade, and Welfare” | Journal article | must-cite | Licensing wedge | Incertidumbre de política | Incertidumbre reduce comercio/entrada | No modela minerales | 10.1257/aer.20141419 | New | Add |
| `fally_2015_structural_gravity_fe` | Fally (2015), “Structural Gravity and Fixed Effects” | Journal article | must-cite | Trade methods | PPML + FE | Fundamento gravity con FE | No trata staggered timing | 10.1016/j.jinteco.2015.05.005 | New | Add |
| `olden_moen_2022_triple_difference` | Olden & Møen (2022), “The Triple Difference Estimator” | Journal article | must-cite | Trade methods | Formalización DDD | Supuesto identificador correcto para DDD | No resuelve pocos shocks | 10.1093/ectj/utac010 | New | Add |
| `conley_taber_2011_small_policy_changes` | Conley & Taber (2011), “Inference with Difference-in-Differences with a Small Number of Policy Changes” | Journal article | must-cite | Few treated shocks | Inference | Problema de pocos cambios de política | No da event-study moderno | 10.1162/REST_a_00049 | New | Add |
| `ferman_pinto_2019_few_treated` | Ferman & Pinto (2019), “Inference in Differences-in-Differences with Few Treated Groups and Heteroskedasticity” | Journal article | must-cite | Few treated shocks | Inference | Pocos tratados + heterocedasticidad | No sustituye placebos | 10.1162/rest_a_00759 | New | Add |
| `mackinnon_webb_2018_few_treated_clusters` | MacKinnon & Webb (2018), “The wild bootstrap for few (treated) clusters” | Journal article | should-cite | Few treated shocks | Inference de respaldo | Bootstrap con pocos clusters tratados | No arregla diseño mal definido | 10.1111/ectj.12107 | New | Add |
| `borusyak_jaravel_spiess_2024_eventstudy` | Borusyak, Jaravel & Spiess (2024), “Revisiting Event-Study Designs” | Journal article | must-cite | Staggered inference | Event-study robusto | Estimación eficiente y robusta | No sustituye DDD principal | 10.1093/restud/rdae007 | New | Add |
| `grossman_helpman_redding_2024_tariffs_supplychains` | Grossman, Helpman & Redding (2024), “When Tariffs Disrupt Global Supply Chains” | Journal article | should-cite | Licensing wedge | Teoría de búsqueda/sustitución | Renegociación y búsqueda de proveedores alternativos | No es sobre licencias chinas | 10.1257/aer.20211519 | New | Add |
| `handley_kamal_monarch_2024_supply_chain_adjustments` | Handley, Kamal & Monarch (2024), “Supply Chain Adjustments to Tariff Shocks” | Journal article | must-cite | Licensing wedge | Evidencia de switching | Respuesta depende de proveedores alternativos | No mide minerales | 10.1016/j.econlet.2024.112009 | New | Add |
| `martin_anderson_2012_price_insulation` | Martin & Anderson (2012), “Export Restrictions and Price Insulation during Commodity Price Booms” | Journal article | must-cite | Price wedge | Precio doméstico vs mundial | Restricciones pueden abrir cuñas de precios | No identifica causalidad mineral china | 10.1093/ajae/aar105 | New | Add |
| `brander_bernauer_huss_2023_tradepolicy_volatility` | Brander, Bernauer & Huss (2023), “Trade policy announcements can increase price volatility…” | Journal article | should-cite | Price wedge | Efecto anuncio e inventarios | Anuncios elevan volatilidad, más con stocks bajos | No es evidencia directa de cuña doméstico-China | 10.1038/s43016-023-00729-6 | New | Add |

### Nuevos candidatos prioritarios

**`unctad_2019_ntm_classification`**
**Full citation:** UNCTAD. 2019. *International Classification of Non-Tariff Measures*. citeturn14search0turn14search3
**Source type:** clasificación oficial.
**Priority:** must-cite.
**Stream:** teoría de licensing wedge.
**Por qué entra:** porque ofrece la distinción formal que tu tesis necesita entre prohibición, cuota y licencia de exportación.
**Uso principal:** fijar vocabulario conceptual en la revisión y en el marco teórico.
**Puede sostener con seguridad:** que *P11* export prohibition, *P12* export quota y *P13* licensing requirement to export son categorías distintas.
**No puede sostener:** que una licencia concreta sea o no binding.
**Download status:** available.
**BibTeX needed:** yes.

**`gamberale_tarasenko_2023_export_licensing`**
**Full citation:** Gamberale, Carlo, & Irina Tarasenko. 2023. *Export Licensing in the WTO Context*. WTO ERSD-2023-06. citeturn34view0
**Source type:** WTO working paper.
**Priority:** must-cite.
**Stream:** teoría de licensing wedge.
**Por qué entra:** explica la licencia como procedimiento administrativo *prior condition for exportation* y subraya que puede añadir restricción adicional si es arbitraria, opaca o gravosa.
**Uso principal:** mecanismo de demora, cumplimiento, opacidad y “trade chilling effect”.
**Puede sostener:** que la licencia es conceptualmente distinta de la restricción sustantiva subyacente y que puede generar costes adicionales.
**Caveat:** es paper institucional/jurídico, no estimación causal.
**Download status:** available.
**BibTeX needed:** yes.

**`prc_2024_dual_use_regulations`**
**Full citation:** State Council / Gov.cn. 2024. Regulations on export control of dual-use items, effective 1 December 2024. citeturn35view0
**Source type:** documento oficial.
**Priority:** should-cite.
**Stream:** instituciones chinas.
**Por qué entra:** actualiza el andamiaje operativo con lenguaje explícito sobre gestión de licencias, listas y supervisión.
**Uso principal:** nota institucional para mostrar continuidad y consolidación del régimen.
**Puede sostener:** que el régimen incluye medidas detalladas de gestión de licencias y supervisión.
**No puede sostener:** efectos comerciales específicos de los episodios 2023–2024.
**Download status:** available.
**BibTeX needed:** yes.

**`oecd_2026_crm_export_restrictions`**
**Full citation:** OECD. 2026. *OECD Inventory of Export Restrictions on Critical Raw Materials 2026*. citeturn37view0turn37view2
**Source type:** reporte oficial.
**Priority:** must-cite.
**Stream:** statecraft / heterogeneidad de producto.
**Por qué entra:** da la mejor base comparativa reciente sobre incidencia global, tipos de medida y exposición por mineral.
**Uso principal:** contextualizar por qué minerales críticos son un espacio de política crecientemente restringido.
**Puede sostener:** aumento cinco veces de las restricciones desde 2009, prevalencia de tasas/licencias, y alta exposición reciente de grafito y otros minerales.
**Caveat:** inventario global; no identifica por sí mismo el efecto causal de China.
**Download status:** available.
**BibTeX needed:** yes.

**`bogdanova_wang_2023_china_export_restrictions_wto`**
**Full citation:** Bogdanova, Iryna, & Anqi Wang. 2023. “China’s Use of Export Restrictions and WTO Law: Heading toward ‘Weaponization’ of Exports?” In *China and the WTO*. citeturn23search1turn23search9
**Source type:** book chapter.
**Priority:** should-cite.
**Stream:** statecraft / China.
**Por qué entra:** ofrece periodización histórica útil para separar fases domésticas de fases geopolíticas.
**Uso principal:** background para la sección de significancia, no para el mecanismo micro.
**Puede sostener:** que la función geopolítica de las restricciones chinas se ha reforzado.
**No puede sostener:** que un producto concreto de 2023–2024 sea binding en el mercado.
**Download status:** available.
**BibTeX needed:** yes.

**`djankov_freund_pham_2010_trading_on_time`**
**Full citation:** Djankov, Simeon, Caroline Freund, & Cong S. Pham. 2010. “Trading on Time.” *Review of Economics and Statistics*. citeturn4search1
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** licensing wedge.
**Por qué entra:** traduce demora administrativa en coste económico.
**Uso principal:** microfundamentar el componente “delay” de la cuña de licencias.
**Puede sostener:** que retrasos fronterizos/administrativos reducen comercio.
**Caveat:** no trata dual-use export licensing de China.
**Download status:** needs verification.
**BibTeX needed:** yes.

**`hummels_schaur_2013_time_trade_barrier`**
**Full citation:** Hummels, David L., & Georg Schaur. 2013. “Time as a Trade Barrier.” *American Economic Review*. citeturn4search3
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** licensing wedge.
**Por qué entra:** refuerza la idea de tiempo como coste comercial, incluso sin prohibición explícita.
**Uso principal:** justificar por qué una licencia que retrasa embarques puede “bind” sin colapsar exportaciones a cero.
**Puede sostener:** que el tiempo tiene valoración económica en comercio.
**Caveat:** evidencia general, no minera.
**Download status:** available.
**BibTeX needed:** yes.

**`handley_limao_2017_policy_uncertainty`**
**Full citation:** Handley, Kyle, & Nuno Limão. 2017. “Policy Uncertainty, Trade, and Welfare: Theory and Evidence for China and the United States.” *American Economic Review*. citeturn5search3
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** licensing wedge.
**Por qué entra:** incorpora el canal de incertidumbre de política, indispensable en una tesis sobre revisión/licencia discrecional.
**Uso principal:** sustentar el término “approval uncertainty”.
**Puede sostener:** que la incertidumbre de política desalienta comercio e inversión/entrada.
**Caveat:** no es sobre controles de exportación chinos de minerales.
**Download status:** available.
**BibTeX needed:** yes.

**`fally_2015_structural_gravity_fe`**
**Full citation:** Fally, Thibault. 2015. “Structural Gravity and Fixed Effects.” *Journal of International Economics*. citeturn38search1turn38search5
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** estrategia empírica trade-flow.
**Por qué entra:** es el mejor puente entre PPML y gravedad estructural con FE.
**Uso principal:** justificar tu especificación saturada de FE.
**Puede sostener:** que PPML con FE es consistente con una interpretación gravity estructural bajo condiciones estándar.
**Caveat:** no discute DDD ni pocos shocks.
**Download status:** available.
**BibTeX needed:** yes.

**`olden_moen_2022_triple_difference`**
**Full citation:** Olden, Andreas, & Jarle Møen. 2022. “The Triple Difference Estimator.” *The Econometrics Journal*. citeturn25search1
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** estrategia empírica trade-flow.
**Por qué entra:** tu estimador central es DDD; esta es la formalización metodológica más directa.
**Uso principal:** defender la lógica identification de la triple diferencia.
**Puede sostener:** la condición correcta de identificación para DDD.
**Caveat:** no es específico a gravedad ni a PPML.
**Download status:** available.
**BibTeX needed:** yes.

**`conley_taber_2011_small_policy_changes`**
**Full citation:** Conley, Timothy G., & Christopher R. Taber. 2011. “Inference with ‘Difference in Differences’ with a Small Number of Policy Changes.” *Review of Economics and Statistics*. citeturn31search0turn31search8
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** inferencia con pocos shocks.
**Por qué entra:** ataca exactamente tu problema de pocos shocks producto-tiempo.
**Uso principal:** limitar la interpretación de p-values clusterizados por importador.
**Puede sostener:** que muchas observaciones no compensan pocos cambios de política.
**Caveat:** marco clásico DiD, no staggered moderno.
**Download status:** available.
**BibTeX needed:** yes.

**`ferman_pinto_2019_few_treated`**
**Full citation:** Ferman, Bruno, & Cristine Pinto. 2019. “Inference in Differences-in-Differences with Few Treated Groups and Heteroskedasticity.” *Review of Economics and Statistics*. citeturn32search0turn32search8
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** inferencia con pocos shocks.
**Por qué entra:** añade el problema de heterocedasticidad, probable en flujos comerciales con tamaños muy desiguales.
**Uso principal:** justificar inferencia conservadora/complementaria.
**Puede sostener:** que pocos tratados + heterocedasticidad invalidan métodos usuales.
**Caveat:** no ofrece solución universal PPML.
**Download status:** available.
**BibTeX needed:** yes.

**`mackinnon_webb_2018_few_treated_clusters`**
**Full citation:** MacKinnon, James G., & Matthew D. Webb. 2018. “The Wild Bootstrap for Few (Treated) Clusters.” *The Econometrics Journal*. citeturn26search19turn26search5
**Source type:** journal article.
**Priority:** should-cite.
**Stream:** inferencia con pocos shocks.
**Por qué entra:** buen complemento práctico para inferencia de respaldo.
**Uso principal:** robustness appendix.
**Puede sostener:** cuándo el wild bootstrap ayuda y cuándo falla con pocos tratados.
**Caveat:** no reemplaza el reconocimiento del problema de diseño.
**Download status:** available.
**BibTeX needed:** yes.

**`borusyak_jaravel_spiess_2024_eventstudy`**
**Full citation:** Borusyak, Kirill, Xavier Jaravel, & Jann Spiess. 2024. “Revisiting Event-Study Designs: Robust and Efficient Estimation.” *Review of Economic Studies*. citeturn28search0
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** staggered/event-study.
**Por qué entra:** es la referencia moderna más fuerte para los diagnósticos dinámicos.
**Uso principal:** event-study por cohortes/olas.
**Puede sostener:** estimación robusta y eficiente con adopción escalonada.
**Caveat:** sigue necesitando una definición correcta de cohortes y ventana.
**Download status:** available.
**BibTeX needed:** yes.

**`grossman_helpman_redding_2024_tariffs_supplychains`**
**Full citation:** Grossman, Gene M., Elhanan Helpman, & Stephen J. Redding. 2024. “When Tariffs Disrupt Global Supply Chains.” *American Economic Review*. citeturn18search1turn18search8
**Source type:** journal article.
**Priority:** should-cite.
**Stream:** adjustment mechanisms.
**Por qué entra:** da la microfundamentación de búsqueda, renegociación y reemplazo de proveedores.
**Uso principal:** marco conceptual del margen de ajuste.
**Puede sostener:** que shocks comerciales no implican colapso mecánico; puede haber switching o renegociación.
**Caveat:** tarifas, no licencias dual-use.
**Download status:** available.
**BibTeX needed:** yes.

**`handley_kamal_monarch_2024_supply_chain_adjustments`**
**Full citation:** Handley, Kyle, Fariha Kamal, & Ryan Monarch. 2024. “Supply Chain Adjustments to Tariff Shocks: Evidence from Firm Trade Linkages in the 2018–2019 U.S. Trade War.” *Economics Letters*. citeturn18search4
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** adjustment mechanisms.
**Por qué entra:** ofrece evidencia empírica directa de que la respuesta depende de proveedores alternativos.
**Uso principal:** justificar heterogeneidad por outside options.
**Puede sostener:** que la vulnerabilidad a shocks depende de concentración de proveedores y capacidad de sustitución.
**Caveat:** no es un estudio de minerales.
**Download status:** available.
**BibTeX needed:** yes.

**`martin_anderson_2012_price_insulation`**
**Full citation:** Martin, Will, & Kym Anderson. 2012. “Export Restrictions and Price Insulation during Commodity Price Booms.” *American Journal of Agricultural Economics*. citeturn20search15turn20search3
**Source type:** journal article.
**Priority:** must-cite.
**Stream:** cuñas de precios.
**Por qué entra:** es la mejor referencia para interpretar divergencias entre precio doméstico y precio mundial.
**Uso principal:** diseño e interpretación del bloque de precios.
**Puede sostener:** que las restricciones pueden aislar o desplazar presión de precios entre mercados.
**Caveat:** commodities agrícolas, no minerales.
**Download status:** available.
**BibTeX needed:** yes.

## Mejora del marco teórico

El marco teórico de propuesta debería quedar así.

**Mecanismo central**. El control chino no se modela como un “ban” automático, sino como una **cuña de licencia** que altera el coste esperado de exportar desde China. Esa cuña combina cuatro componentes: riesgo de demora o no aprobación, coste de documentación y compliance, incertidumbre sobre reglas y enforcement, y menor disponibilidad efectiva desde China en el margen. La literatura de NTMs y de OMC permite separar la licencia de la prohibición; la literatura de tiempo y de incertidumbre comercial permite traducir esa separación jurídica en un shock económico mensurable. citeturn14search0turn34view0turn4search3turn5search1turn5search3

**Moderadores a nivel producto**. Los efectos deberían ser más fuertes cuando el producto tiene mayor concentración de oferta, pocas alternativas de sustitución, mayor dependencia de coproductos/host metals y alcance regulatorio más limpio. Nassar, Graedel, Frenzel e IEA implican una predicción clara: los minerales críticos con alta companionality, alto poder de mercado en procesamiento y baja sustituibilidad son los candidatos más plausibles a mostrar binding observable. La OCDE añade que grafito, tierras raras y otros minerales ya operan en mercados con exposición elevada a restricciones. citeturn21search9turn21search1turn11search1turn12search8turn37view2

**Moderadores a nivel importador**. La respuesta debe depender de la capacidad de ajuste del comprador. La teoría y la evidencia sobre shocks arancelarios y cadenas de suministro apuntan a tres casos: importadores con buenas outside options pueden reasignar sourcing; importadores sin alternativas cercanas sufren contracción de importaciones totales; importadores con stocks o anticipación pueden mostrar efectos retardados o amortiguados. En tu tesis, esos moderadores son observables imperfectos, no parámetros estructurales: exposición previa a China, concentración de proveedores alternativos, supplier count/HHI y timing de anticipación. citeturn18search1turn18search4turn20search17

**Márgenes esperados de ajuste**. El primer margen es la caída de importaciones desde China en el producto tratado. El segundo es el *switching* hacia resto del mundo. El tercero es la contracción de importaciones totales si la sustitución falla. El cuarto es una cuña de precios doméstico–internacional o China doméstico–benchmark internacional cuando la segmentación de mercado se amplía. Esta arquitectura encaja mejor con un mundo de licencias y fricciones administrativas que con una historia binaria de “export control = export collapse”. citeturn34view0turn18search1turn18search4turn20search15turn20search17

**Diferencia frente a la narrativa simple**. El salto conceptual importante es este: dos controles “formalmente similares” pueden producir efectos diferentes porque lo relevante no es solo el texto legal, sino la interacción entre diseño administrativo, estructura de mercado, productos coproducto, inventarios y capacidad de sustitución del importador. Esa es la razón correcta para hablar de **binding heterogéneo**. citeturn34view0turn11search1turn21search9turn18search4turn20search17

## Mejora de la estrategia empírica

| Design Element | Current Plan | Existing Support | Missing/Needed Source Support | Recommended Source(s) |
|---|---|---|---|---|
| Source-share PPML triple difference | PPML DDD con FE de alta dimensión | `santossilva2006gravity` | Fundamento gravity con FE y formalización DDD | `fally_2015_structural_gravity_fe`; `olden_moen_2022_triple_difference` |
| Wave-specific DDD | Estimar por cohortes de tratamiento | `callaway2021difference` | Relación entre staggered timing y lógica DDD | `olden_moen_2022_triple_difference`; `borusyak_jaravel_spiess_2024_eventstudy` |
| Staggered/event-study diagnostics | Cohorts/event-study | `callaway2021difference`; `sun2021eventstudies` | Referencia robusta y eficiente más reciente | `borusyak_jaravel_spiess_2024_eventstudy`; `baker_callaway_cunningham_goodmanbacon_santanna_2026_did_guide` |
| Price-wedge DiD/event study | Comparar precio doméstico chino vs benchmark internacional | ninguno claramente suficiente | Teoría de price insulation/market segmentation y metodología de benchmarks | `martin_anderson_2012_price_insulation`; `brander_bernauer_huss_2023_tradepolicy_volatility`; Banco Mundial Pink Sheet / IMF PCPS |
| Switching-potential heterogeneity | Heterogeneidad por outside options, HHI, supplier count | `frenzel2017byproduct_metals`; `iea_2025_global_critical_minerals_outlook` | Evidencia de reajuste de sourcing ante shocks comerciales | `handley_kamal_monarch_2024_supply_chain_adjustments`; `grossman_helpman_redding_2024_tariffs_supplychains` |
| Donor-pool and placebo diagnostics | Placebos por producto y screening de donantes | `rambachan2023honest`; `roth2022pretest` | Inferencia placebo/permutación con pocos tratados | `hagemann_2019_placebo_inference`; `shaikh_toulis_2021_randomization_tests` |
| Inference limits with few product-level treatments | p-values clusterizados por importador como diagnóstico condicionado | ninguno directo | Literatura de pocos shocks/pocos tratados | `conley_taber_2011_small_policy_changes`; `ferman_pinto_2019_few_treated`; `mackinnon_webb_2018_few_treated_clusters` |

**Recomendación metodológica nítida**. Mantén el **PPML DDD** como estimador principal, pero refuérzalo con tres piezas. Primera, explícita la lógica DDD con Olden y Møen. Segunda, trata los event studies como diagnósticos staggered modernos, preferentemente con una implementación robusta al estilo Borusyak–Jaravel–Spiess además de la intuición Callaway/Sun-Abraham. Tercera, deja por escrito que, dado que la variación de política descansa en un número pequeño de shocks producto-tiempo, la inferencia principal debe incluir **placebos/permutaciones a nivel producto** o métodos diseñados para pocos tratados, y que el clustering por importador no es suficiente como solución inferencial final. citeturn25search1turn28search0turn31search0turn32search0turn26search19turn29search3turn29search7

**Recomendación sobre precios**. El bloque de precios debe entrar en la propuesta, pero no como “prueba principal” del efecto. Debe presentarse como evidencia de mecanismo/corroboración, condicionada a una estricta armonización de tipo de producto, pureza/grado, ubicación del benchmark, unidad física, moneda e incoterm. Las bases oficiales de benchmarks dejan claro que estos atributos definen la serie misma; por eso una cuña de precios mal armonizada puede contaminarse con diferencias de calidad o base de cotización y no solo con segmentación de mercado. citeturn33search0turn33search1turn20search15

## Vacíos restantes, checklist de adquisición y próximos pasos

### Vacíos de búsqueda todavía abiertos

Quedan cinco vacíos concretos.

Primero, falta una **fuente académica fuerte y específica sobre grafito** comparable a lo que Frenzel hace para gallio/germanio/indio. El corpus actual tiene suplementos, pero su estado editorial debe verificarse.

Segundo, falta una **fuente específica sobre metodología de precios** para las series que realmente vayas a usar en galio, germanio, grafito y antimonio. Las referencias de Banco Mundial/IMF sirven como disciplina metodológica general, pero no sustituyen las fichas metodológicas del proveedor concreto de precios si vas a usar series comerciales especializadas. citeturn33search0turn33search1turn33search13

Tercero, convendría añadir una referencia directamente conectada con **gravity + staggered DiD** en comercio si finalmente el capítulo metodológico quiere formalizar más ese puente. El working paper sobre staggered DiD en gravity settings parece prometedor, pero puede dejarse como `deferred` para no inflar el corpus activo. citeturn38search12

Cuarto, si la muestra se amplía a 2025, hará falta un bloque propio sobre **rare earths y la segunda ola**; por ahora debe quedar fuera del corpus activo para no contaminar el diseño base.

Quinto, siguen faltando **fuentes de adquisición de datos operativos** para proxies de anticipación e inventarios. La literatura sugiere que stocks importan para la dinámica del precio, pero la tesis aún no tiene una estrategia de medición fuerte para ese canal. citeturn20search17

### Source Acquisition Checklist

| Target Source | Priority | Zotero | PDF/HTML | Source Folder | Summary Needed | Notes |
|---|---|---|---|---|---|---|
| UNCTAD NTM classification | High | Add | PDF | `unctad_2019_ntm_classification` | Yes | Fundacional para separar licencia/prohibición/cuota |
| WTO export licensing paper | High | Add | PDF | `gamberale_2023_export_licensing_wto` | Yes | Núcleo del mecanismo administrativo |
| PRC dual-use regulations 2024 | Medium | Add | HTML/PDF if available | `prc_2024_dual_use_regulations` | Short | Complemento institucional |
| OECD CRM export restrictions 2026 | High | Add | PDF | `oecd_2026_crm_export_restrictions` | Yes | Contexto global y tipología de medidas |
| Bogdanova & Wang 2023 | Medium | Add | PDF/HTML | `bogdanova_wang_2023_export_restrictions_wto` | Short | Periodización histórica China |
| Djankov et al. 2010 | High | Add | PDF | `djankov_freund_pham_2010_trading_on_time` | Yes | Demora como coste |
| Hummels & Schaur 2013 | High | Add | PDF | `hummels_schaur_2013_time_trade_barrier` | Yes | Tiempo como barrera |
| Handley & Limão 2017 | High | Add | PDF | `handley_limao_2017_policy_uncertainty` | Yes | Incertidumbre de política |
| Fally 2015 | High | Add | PDF | `fally_2015_structural_gravity_fe` | Yes | PPML + FE |
| Olden & Møen 2022 | High | Add | PDF | `olden_moen_2022_triple_difference` | Yes | DDD |
| Conley & Taber 2011 | High | Add | PDF | `conley_taber_2011_small_policy_changes` | Yes | Pocos shocks |
| Ferman & Pinto 2019 | High | Add | PDF | `ferman_pinto_2019_few_treated` | Yes | Pocos tratados + heterocedasticidad |
| MacKinnon & Webb 2018 | Medium | Add | PDF | `mackinnon_webb_2018_few_treated_clusters` | Short | Bootstrap como respaldo |
| Borusyak et al. 2024 | High | Add | PDF | `borusyak_jaravel_spiess_2024_eventstudy` | Yes | Event study robusto |
| Handley et al. 2024 | High | Add | PDF | `handley_kamal_monarch_2024_supply_chain_adjustments` | Yes | Switching / outside options |
| Grossman et al. 2024 | Medium | Add | PDF | `grossman_helpman_redding_2024_tariffs_supplychains` | Short | Microfundamentos de ajuste |
| Martin & Anderson 2012 | High | Add | PDF | `martin_anderson_2012_price_insulation` | Yes | Price wedge / insulation |
| Brander et al. 2023 | Medium | Add | PDF | `brander_bernauer_huss_2023_tradepolicy_volatility` | Short | Anuncios e inventarios |
| Price methodology docs for actual benchmark provider | High | To collect | HTML/PDF | provider-specific | Yes | Vacío todavía abierto |
| Verify `park2025graphite_supply_chain` / `vandenbrink2022antimony_resilience` / `xu2025antimony_material_flow` | Medium | Verify | Unknown | existing folders | Maybe | No tratarlas como centrales sin verificación |

### Siguientes pasos sugeridos

Para `02_literature/references.bib`, la prioridad es añadir primero los **diez nuevos must-cite** y limpiar las claves publicadas/working-paper dudosas. En particular: crear entradas nuevas para UNCTAD, WTO, OECD 2026, Djankov, Hummels, Handley & Limão, Fally, Olden & Møen, Conley & Taber, Ferman & Pinto y Borusyak et al.; y revisar `roth2022pretest`.

Para `02_literature/sources/`, separa físicamente tres carpetas raíz: `academic/`, `official/` y `market_data_methodology/`. Las guías de licencia de MOFCOM y la ley china deben quedar en `official/`; la teoría y métodos en `academic/`.

Para `02_literature/summaries/`, prioriza resúmenes analíticos breves y funcionales. Cada resumen debería responder solo a cuatro preguntas: qué sostiene, qué no sostiene, qué variable/mecanismo alimenta en la tesis y qué limitación tiene.

Para la **literature review** de la propuesta, reorganiza el texto en el mismo orden de corrientes usado aquí. Eso evita la forma “source dump” y alinea teoría, instituciones, estructura de mercado y método con la lógica real de la tesis.

Para la **sección de marco teórico**, introduce explícitamente la ecuación verbal: **binding licensing wedge = delay/denial risk + compliance cost + uncertainty + reduced Chinese availability**, y luego deriva de ella los cinco resultados observables: caída China-source, switching hacia ROW, contracción total, cuña de precios y heterogeneidad por producto/importador. Esa es la pieza que hoy más diferencia una tesis de un term paper. citeturn34view0turn4search3turn5search3turn18search4turn20search15

Para la **sección de estrategia empírica**, deja por escrito desde la propuesta que: el estimador principal es PPML DDD; los event studies serán diagnósticos staggered robustos; y la inferencia central incorporará sensibilidad a pocos shocks y placebos/permutaciones a nivel producto, precisamente porque el número de shocks de política independientes es pequeño. citeturn25search1turn28search0turn31search0turn32search0turn29search3

### Open questions y limitaciones

No he verificado en esta sesión el contenido exacto de los archivos locales `literature_master.md`, `references.bib` y notas del repositorio, así que cualquier cruce fino con claves ya existentes debe hacerse al integrar el documento en Zotero/BibTeX.

Tampoco he verificado todavía la metodología del proveedor de precios que efectivamente usarás para las series minerales. Ese punto sigue siendo la principal limitación del bloque de price wedge.

Por último, la propuesta puede centrarse limpiamente en 2023–2024. Si luego decides ampliar la muestra a 2025, el corpus necesitará un segundo bloque propio para tierras raras y para las medidas bilaterales/suspensiones de 2025, pero **no conviene mezclarlo ahora** con el diseño base.