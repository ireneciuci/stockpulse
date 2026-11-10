"""One-off: seed labels for the first batch (produced by Claude in the build session).
Anything not listed is marked not relevant. Future batches are scored via the API."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import db
L = {
# AAPL
"e807231488bc4fb7": (.6,3,"other","Market cap passes $5T on record close above $350"),
"eca034159a69d33c": (-.3,3,"management","AI/Siri timelines slip; possible engineering leadership change"),
"952db49917be9190": (.4,2,"macro_sector","TSMC sales jump on Apple and Nvidia orders"),
"afbd02919355d32b": (.1,1,"other","ETF flow: Apple led TECL buys"),
"be5144bfbeda0eaf": (.1,1,"other","ETF flow: Apple led QQQ buys"),
"2bc24adbfa276db0": (-.1,1,"other","ETF flow: IXN sold $26.8M of Apple"),
"30e70b96529fe727": (0,2,"filing_routine","8-K other material event filed"),
"992632cad0085757": (.2,3,"earnings","Quarterly earnings 8-K filed"),
# AMD
"6a461937dad12463": (.6,3,"guidance","Revenue guidance now exceeds Intel's"),
"ebf4f34e40c4f0a1": (.3,3,"deal_mna","Part of $26B big-tech investment in Anthropic IPO"),
"12a56321f7afe9b5": (-.2,1,"other","Seen opening lower pre-market after rally"),
"66c377d4409f14c9": (-.1,2,"other","Burry declines to chase 13% surge"),
"da5cc80863d6b310": (-.1,1,"other","ETF flow: SOXX net seller of AMD"),
"3859abc24d478523": (-.1,1,"other","ETF flow: net selling of AMD"),
"cc9169125553544b": (.5,2,"product","Seen closing competitive gap with Nvidia"),
"d49ca4e8b32c4eae": (.4,4,"earnings","Q3 earnings 8-K and Reg FD disclosure"),
# AMZN
"52e5debb8e427aae": (.2,1,"product","Custom silicon strategy analysis"),
"b7316f5b385a07ed": (-.4,2,"legal_regulatory","Potential trial in Italy over Chinese imports"),
"107269bc03fbe061": (.1,1,"other","ETF flow: $159M bought"),
"c00552797357d2e4": (.2,3,"earnings","Quarterly earnings 8-K filed"),
# BA
"f904514146d8b705": (-.2,2,"earnings","Earnings described as underwhelming"),
"6ef139b9670d0e75": (-.3,3,"management","Cutting 5% of commercial workforce"),
"c6ce57810fd27697": (.2,2,"deal_mna","Archer deal with Boeing close imminent"),
"47877548cf151fc9": (.5,3,"product","Record jet order lands"),
"8931dbccbe28157b": (-.4,3,"management","Layoffs while struggling to raise production"),
"7e8baba33de29d2b": (-.3,2,"management","Stock lower on 5% workforce cut report"),
"c623659138722f06": (-.3,2,"management","Workforce decision as production slows"),
"765fe5a571e73d02": (-.2,1,"other","Retiree health insurance cost hike"),
"2a19c28601be62f2": (-.3,3,"management","Cutting 5% of commercial airplane workforce"),
"90f87c734f475c86": (0,3,"earnings","Quarterly earnings 8-K filed"),
# DIS
"9c891faf6a76a929": (.4,3,"earnings","Next earnings get one-off $600M boost"),
"542f1b7c3ea5aaeb": (.1,1,"product","AI push analysis"),
"ae9456ce5944f4d4": (.1,1,"other","Gained but lagged market"),
"148aaa3632ce6bdf": (.2,2,"product","Weighs free tier to lift Disney+ engagement"),
"b98a010cfbd8cece": (0,2,"product","Adobe AI deal amid reported job cuts"),
"9c33d55f909468bc": (.3,2,"deal_mna","Multi-year Adobe AI alliance"),
"e4acda336d9d39dd": (-.3,2,"other","Losing ground to Netflix"),
"c5636cefcab43305": (.1,3,"management","Eyes 20% cost cuts, thousands of layoffs"),
"56cc666079b956b8": (.1,1,"other","Valuation: fairly valued, cash flow holds"),
"db6afddd8e255ad4": (.3,1,"other","Opinion: long-term bull case"),
# GOOGL
"19ea5d20bf94b717": (-.1,2,"deal_mna","Anthropic (Google-backed) retracts leaked IPO range"),
"d88ac797ca9f2b5c": (.3,1,"other","Opinion: 30% upside case"),
"1aa09d7011e7a856": (.3,1,"other","Valuation below Berkshire's entry price"),
"0bf381d5aed7e176": (.1,1,"product","Google Cloud partnership with FlowX.AI"),
"1877b1518b675eb5": (.6,3,"product","Strong Google Cloud update from Pichai"),
"1bfcb98d6647aa62": (.2,1,"product","Custom silicon strategy analysis"),
"a1186a949101bef6": (.3,3,"deal_mna","Investing in Anthropic alongside IPO"),
"414a216accae873d": (.2,2,"deal_mna","Anthropic $90B raise includes big tech placement"),
"5ba8665a55465b70": (0,2,"filing_routine","8-K other material event filed"),
"729a2343498ece14": (.2,3,"earnings","Quarterly earnings 8-K filed"),
# INTC
"34491bfcb5f87c65": (.3,2,"other","Explainer on Intel's share price rise"),
"fbf3cc5113524f5c": (-.4,2,"other","AMD now guides more revenue than Intel"),
"a9fda8c10ffad99b": (-.1,1,"other","ETF flow: net selling of Intel"),
"1b0128628ae52c65": (.4,2,"macro_sector","Chip shares including Intel soaring"),
"555d4ea0e18d2a22": (-.4,2,"other","Gave back dot-com-peak recovery within 6 months"),
"258b8f0d68f866aa": (0,3,"earnings","Quarterly earnings 8-K filed"),
# JPM
"0635a0d3785c8cfb": (0,1,"capital_return","Routine ETF distributions"),
"76e842caf551be70": (-.2,3,"legal_regulatory","Senate probe news; valuation called 31% undervalued"),
"bfd013e5c47ce26d": (.2,2,"deal_mna","Dimon on Anthropic IPO live stream (likely deal role)"),
"85a15f5bfd5aedbf": (.4,2,"macro_sector","Bank stocks rally, JPM +2%"),
"8cbf54e2c695d122": (0,1,"other","Hall of Innovation award"),
# KO
"d2e6d855bd05c4f2": (.3,1,"capital_return","Opinion: 64 years of dividend growth"),
"b1330cca8939ccd3": (.1,1,"product","Bottler system tech rollout"),
"196f8a4687d37aa8": (.4,3,"deal_mna","Coca-Cola India IPO draft papers filed"),
"d56ca653a30f964e": (-.1,1,"other","Opinion: record highs, author not buying"),
"3e1410541afa64b6": (.2,1,"capital_return","Dividend yield on Buffett's cost"),
"72996f59f873fdb9": (.1,2,"other","Volume growth, but on low-upside list"),
"fa497cfa9b17afef": (.2,3,"earnings","Quarterly earnings 8-K filed"),
# LLY
"524c11b88a6ff902": (.1,1,"product","Foundayo patient marketing story"),
"41761410ddd4360b": (-.1,2,"legal_regulatory","FDA vision-loss warning; shares unfazed"),
"ab6f04b3bf0a3ab3": (.1,1,"other","Zacks industry highlight"),
"bf42f7ce56d603a2": (.4,1,"other","Cramer: a $2 trillion stock"),
"53ef042410294e7c": (.5,3,"product","Weight-loss pill shows sleep apnea benefit"),
"4121b19f919bf858": (.7,3,"analyst_rating","Jefferies street-high $1,700 target, stock +3.4%"),
"4914e2584c4fdca5": (-.3,3,"legal_regulatory","FDA requires vision-loss warning on GLP-1 drugs"),
"70e4403009fa1c56": (.6,4,"product","Phase III sleep apnoea trial win for Foundayo"),
"99b1ccfb24e39847": (.5,2,"product","New $23B market for GLP-1 pill"),
"4aed41464e7aed18": (.3,3,"earnings","Quarterly earnings 8-K filed"),
# META
"28e397921afd2795": (.3,2,"product","VR glasses first IMAX-certified VR device"),
"4e3e908539dd82b2": (.1,1,"product","Pixelworks partnership for VR glasses"),
"c8e706621061d0ee": (.1,1,"other","ETF flow: $212M bought"),
"cbda2e0179d24e97": (.1,1,"other","Opinion: Mag 7 cash-flow ranking"),
"98cb915a4977766d": (.3,2,"product","Teaming with Alphabet/Oracle vs Nvidia moat"),
"644c4c2fb1e62784": (-.4,2,"product","Chase blocks Meta Muse, called malware-like"),
"63064b152e109396": (-.3,2,"capital_return","No buybacks in 2026"),
"f2f4d4376045bb53": (.3,1,"other","Opinion: cheap at $650"),
"40c5317fad17504d": (0,2,"filing_routine","8-K other material event filed"),
"c78ae57b37f77eb8": (0,3,"governance_scandal","8-K: material agreement and charter amendment"),
# MSFT
"99e2a2319eaf0d65": (.4,2,"product","New AI agent platform with IBM"),
"55d49c05600ca364": (.4,2,"product","IBM partnership on AI agents"),
"7fb4c9a0e329f678": (-.3,3,"legal_regulatory","Chinese optics ban could slow data center rollout"),
"ad3cfbe8e8ddb33d": (.3,1,"legal_regulatory","Opinion: winning regulatory shift"),
"ca4e697c8d8093d3": (.2,2,"deal_mna","Big-tech investment in Anthropic IPO"),
"3c0ecfa5ec486aab": (-.3,3,"legal_regulatory","Lobbying against Chinese component ban (supply risk)"),
"c7af1578e9bd0735": (-.1,1,"deal_mna","Anthropic IPO cut after pricing mix-up"),
"da9196009aae883e": (0,2,"management","8-K executive / board change"),
"92424e2601d1876d": (0,2,"filing_routine","8-K other material event filed"),
"99f50c2401279491": (0,2,"filing_routine","8-K other material event filed"),
"b4cb097a645799c6": (.3,3,"earnings","Quarterly earnings 8-K filed"),
# NFLX
"41f1c67aff3ea632": (.2,1,"deal_mna","AMC Networks content deal with Netflix"),
"54318f4e852ab0bc": (-.5,3,"other","Stock plunged 11% in October"),
"a88d4ae02ac3526e": (-.2,2,"legal_regulatory","CEO warns on European regulation"),
"776ae73c941fcab6": (.2,1,"other","Opinion: 10-year hold"),
"1266cfd5492584f6": (.1,1,"product","IMAX premium screens for Netflix release"),
"c7fea57774c85be9": (0,1,"other","Search-trend explainer"),
"335ac75f6f3b8ac2": (.3,2,"other","Valuation: 23% upside to fair value"),
"536ba91977e668b8": (.4,2,"other","Pulling away from Disney"),
# NVDA
"ddf86c3a2ea3cdf2": (-.6,4,"governance_scandal","Short seller flagged CEO ties before scandal"),
"2c0eaef508bb59bb": (-.6,4,"governance_scandal","CEO personal scandal may prove costly"),
"720c7a21c941f1e9": (-.6,4,"analyst_rating","BofA drops Nvidia from top-picks list"),
"bdb52cbd9f97420c": (-.4,3,"governance_scandal","New risks for Nvidia and chip ecosystem"),
"c73a34535ec737fc": (-.4,3,"governance_scandal","Scandal collides with Anthropic IPO"),
# PFE
"3a7108209f94ae96": (.6,2,"other","Hits new 52-week high"),
"2390a2f04dcaf133": (.2,1,"deal_mna","Out-licensed ADC to Medicus"),
"6d2cd0e11e2ccf8f": (.4,2,"guidance","Higher 2026 outlook looks achievable"),
"2e03eae38d0cff74": (-.2,1,"other","Valuation: overvalued after 29% gain"),
"b2bdd642c1d04225": (.3,2,"product","GLP-1 leadership plan, launch not before 2028"),
"1b86a3ae4550250d": (0,1,"other","Attention explainer"),
"6b029e8c1690690f": (-.3,2,"other","Patent-cliff risk analysis"),
"1c7c519993421de9": (.4,2,"product","Planning wave of Phase 3 obesity trials"),
"ede29ab4d3a29bbb": (.1,1,"other","Listed among AI healthcare stocks"),
"6d8cad658f1c582c": (0,2,"management","8-K executive / board change"),
"8759557d363470a3": (.3,3,"earnings","Quarterly earnings 8-K filed"),
# TSLA
"3f6af1326314df71": (.3,2,"other","Musk seen gaining as Nvidia stumbles"),
"a079ba935aacbc53": (.1,1,"other","ETF flow: ETFs buying Tesla"),
"2378887799bee23d": (0,1,"other","Opinion: Mag 7 ranking"),
"41124e717f9cdad0": (-.3,2,"product","Uber/Waymo seen threatening robotaxi lead"),
"147e78a8bc1f8876": (.3,2,"management","Musk sends bullish signal"),
"33a9d51115868f8c": (.4,2,"other","Tesla rallies as Dow jumps 1,132 points"),
"5dbcbeda8000b31f": (-.4,3,"product","Must refund many Cybertruck deposits"),
"991fa5f59fea10b8": (-.2,1,"product","Cybertruck production shortfall"),
# UNH
"062bb0694f6c208c": (.4,3,"guidance","Among Q3 companies raising guidance"),
"5beaae1f9f34f562": (.1,1,"management","New board director Madeline Bell"),
"59785e58850b4cbe": (.0,2,"management","8-K board change"),
"2c50bb081ba5cf61": (.3,1,"other","Profit margins improving"),
"300cec8b225bb347": (.1,1,"other","Broken stock with turnaround catalysts"),
"5e8c62253a438191": (.4,2,"other","Margin repair starting to show"),
"82a58922c8fc8ff0": (.1,1,"other","Listicle post-midterms"),
"fbf8c0e5300aa0c5": (.2,1,"other","Institutional buying"),
"7393e8bb5f74dadb": (-.6,4,"legal_regulatory","Warren targets UNH breakup after Democrats win Congress"),
"2a9ac362659f2ea3": (0,1,"other","Peer comparison with Humana"),
"e99b724390d8ea6b": (-.5,3,"legal_regulatory","Lost ground on Medicare star ratings"),
"0dee446267052ef1": (.3,1,"analyst_rating","Analysts rate Buy"),
"dc9d80e061b89e84": (.1,1,"other","ETF flow: ETFs buying"),
# V
"70ea76c07352ef1d": (0,1,"other","Key dates explainer"),
"0723a400892804d3": (.5,3,"earnings","20%+ services growth; US volume momentum"),
"2a615131be3f3465": (-.1,1,"other","ETF flow: net selling"),
"ef13c1f017be5eaa": (.1,1,"analyst_rating","Analyst outlook roundup"),
"064e92c2f34ba35c": (.4,2,"earnings","15% revenue growth, 7% analyst upside"),
"c944a72438160485": (.1,2,"earnings","Strong Q4 but valuation questions"),
"94913e6ce319171c": (.5,3,"capital_return","Dividend raised 16%"),
"d32b43b34326938c": (.4,2,"capital_return","16% dividend hike; buyback capacity"),
"9bb15e106b937243": (.3,3,"earnings","Quarterly earnings 8-K filed"),
# WMT
"8c54d369717085da": (-.1,1,"other","ETF flow: XLP sells Walmart"),
"2476b4630817bf99": (.1,1,"other","ETF flow: 51 ETFs add WMT"),
"c5789fb5aaf62537": (.1,1,"other","Premium valuation vs Target"),
"4f973201f5bab198": (-.3,2,"other","Unusual put volume before earnings"),
"a968f56a30fccaf4": (.5,2,"analyst_rating","UBS sees earnings upside beyond sales"),
"e9a311d7541eb5a0": (-.1,1,"legal_regulatory","Settlement refund checks going out"),
"7b4b0d9faa8b0b76": (.3,2,"product","Expands into home energy and healthcare"),
"0423baa29b9e1287": (-.1,1,"macro_sector","Instacart cites Walmart as competition"),
"73e2b8027c36516b": (-.1,1,"other","ETF flow: XLP sold $44M"),
# XOM
"2406c88bd2b9ba8d": (.2,1,"capital_return","Cash return analysis"),
"df54ff98bd12c85a": (.2,3,"deal_mna","MoU with Venezuela on oil investment"),
"4bb78857c7e662e3": (.1,1,"other","Near record highs; historical view"),
"c1ee9a3ca1a040b9": (-.2,2,"macro_sector","Crude slides toward $87"),
"ffb76f520c925857": (-.3,2,"product","Pauses Texas hydrogen facility"),
"c14b6e5c2e975479": (-.1,2,"macro_sector","OPEC+ holds output; crude lower"),
"caf45fc0d6842348": (.1,1,"other","Q3 production comparison"),
"6fdfd450984064af": (-.1,1,"other","ETF flow: IXC selling"),
"eec2645d18d9a4a3": (.3,1,"other","Up 38% in 2026"),
"5df178aa0adedf00": (.2,3,"earnings","Q3 earnings key metrics"),
"6c4b3fa499d5b82c": (.2,3,"earnings","Quarterly earnings 8-K filed"),
}
con = db.connect()

# Articles that surfaced in one ticker's feed but are really about another company.
# The analyst agent handles this via "also_about"; for the seed batch we map them by hand.
EXTRA = {
("3f139f9f51ab8ebe","NVDA"): (-.8,5,"governance_scandal","CEO admits affair; company opens probe into spy claims"),
("526d637adbd1315c","NVDA"): (-.5,4,"governance_scandal","Debate on ousting CEO after scandal"),
("4e404124cf9bb6df","NVDA"): (-.3,3,"governance_scandal","More bad news for CEO; Cathie Wood still bullish"),
("33a9d51115868f8c","NVDA"): (-.5,3,"other","Nvidia dives while Dow soars 1,132 points"),
("254ff8754270f81a","NVDA"): (-.2,2,"macro_sector","Chip stocks rally while Nvidia lags"),
("9a802633d8eddc68","NVDA"): (-.2,2,"other","Nasdaq-100 best day since March without Nvidia"),
("952db49917be9190","NVDA"): (.4,2,"macro_sector","TSMC sales jump on Apple and Nvidia orders"),
("a1186a949101bef6","NVDA"): (.2,3,"deal_mna","Investing in Anthropic alongside IPO"),
("65ac97ddc769c4e7","META"): (.6,3,"analyst_rating","JPM top internet pick; stock +5%"),
("5f78f2b5e120ec48","META"): (.7,3,"analyst_rating","JPMorgan bets on AI ad growth; stock +4.8%"),
("f670a7ce61691a71","META"): (.6,3,"analyst_rating","Added to JPMorgan focus list"),
("65ac97ddc769c4e7","AMZN"): (.6,3,"analyst_rating","JPM top internet pick; stock +5%"),
("990b87972fee3275","GOOGL"): (-.4,3,"analyst_rating","JPMorgan removes Alphabet from focus list"),
("16875d8b2e13f279","AMD"): (.7,4,"analyst_rating","Oppenheimer upgrade; chosen for Google Cloud chips"),
("0c974446ca4b05f9","AMD"): (.4,3,"guidance","Eased Wall Street's AI spending worries"),
}
import hashlib
for (src, t), lab in EXTRA.items():
    a = con.execute("SELECT * FROM articles WHERE id=?", (src,)).fetchone()
    nid = hashlib.sha1(f"{t}|{a['url']}".encode()).hexdigest()[:16]
    con.execute("INSERT OR IGNORE INTO articles VALUES (?,?,?,?,?,?,?,?,?)",
                (nid, t, a["title"], a["url"], a["source"], a["source_type"], a["published_at"], a["summary"], a["fetched_at"]))
    L[nid] = lab
con.commit()
out = {}
for r in con.execute("SELECT id, ticker, title FROM articles"):
    if r["id"] in L:
        s, m, e, why = L[r["id"]]
        out[r["id"]] = dict(relevant=True, sentiment=s, materiality=m, event_type=e, reason=why, model="claude-seed")
    else:
        out[r["id"]] = dict(relevant=False, sentiment=0, materiality=1, event_type="other",
                            reason="Not mainly about this company", model="claude-seed")
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "data", "analyst_labels.json"), "w"), indent=0)
print(len(out), "labels,", sum(v["relevant"] for v in out.values()), "relevant")
