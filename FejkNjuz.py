import requests

BASE_URL = "http://127.0.0.1:8000"

reg = requests.get(f"{BASE_URL}/")
print(reg.json())


reg = requests.get(f"{BASE_URL}/model_summary")
print(reg.json()["Summary"])

reg = requests.get(f"{BASE_URL}/model_languages")
print(reg.json())

article = """
Irish PM at Davos: 'Fight for Ukraine is a fight for wider European values'

Taoiseach Leo Varadkar says he believes the European Council will vote to approve a pending €50 billion Ukraine fund in February.

Ireland's prime minister says that a fight for Ukraine is a "fight for wider European values." 

Taoiseach Leo Varadkar made the comments in a Euronews interview at the annual World Economic Forum meeting in Davos, Switzerland, on Thursday. 

"We stand with Ukraine for as long as it takes, and Ukraine needs financial support from the European Union and the US and other allies," he said. 

Varadkar said he believes it will be possible for the European Council to approve a new €50 billion package of grants and loans for Ukraine at its next meeting on 1 February. 

But he says if it is not possible for the EU to come to an agreement - with Hungary stalling the process so far - then individual countries should act together to provide the assistance Ukraine needs.  

"I'd much prefer to see us do it on the basis of unanimity. But we have to have a plan B and a fallback option. And to me that would be the governments that are willing and able to support Ukraine [...] would do so on a multilateral basis." 

Varadkar said the "vast majority" of governments in Europe are in favour of passing the European Council's €50 billion package for Ukraine. 

Earlier this week, the President of the European Commission Ursula von der Leyen said the EU will find a way, if needed, to bypass Hungarian PM Viktor Orbán's veto and approve the €50-billion special fund for Ukraine.


The package, which is designed to provide Kyiv with financial support until 2027 and plug the government's ballooning public deficit, is being held up by Hungary, an impasse that has left Brussels effectively without any money for the war-torn nation.

Following a dramatic summit in mid-December, where Orbán made good on his threat and derailed the unanimous vote, EU leaders are set to reconvene again on 1 February to give the so-called Ukraine Facility a second try.

"I think it's very important to engage with all 27 member states of the European Union to get the €50 billion for four years for Ukraine up and running," von der Leyen told journalists, including Euronews, in Davos on Tuesday.


"""


article2 = """
Woman killed in Aurora while on phone with her sister
A woman reported that she heard her sister get shot over the phone
Police found a woman had been shot and killed on Thursday evening after her sister reported hearing the shooting over the phone. 

Aurora officers responded to a shooting report in the 10700 block of East Exposition Avenue around 7 p.m. on Thursday. Responders found a woman with a gunshot wound within the residence. She died at the scene, according to the Aurora Police Department.

The 911 caller said she was on the phone with her sister when she heard an argument. She then heard gunshots and called the police.
No suspect has been identified and no arrests have been made, according to the police. Crime Scene Investigators and Major Crime Homicide Unit detectives are investigating the incident.

Anyone with any information about the incident is asked to contact Metro Denver Crime Stoppers at 720-913-7867.

This story is developing
"""

reg = requests.post(f"{BASE_URL}/predict_from_text", json={"text": article})
print(reg.json())

reg = requests.post(f"{BASE_URL}/predict_from_text", json={"text": article2})
print(reg.json())


reg = requests.post(f"{BASE_URL}/predict_from_url", json={
    "article_url": "https://www.euronews.com/2024/01/18/irish-pm-fight-for-ukraine-is-a-fight-for-wider-european-values",
    "trim": True
})
print(reg.json())


reg = requests.post(f"{BASE_URL}/predict_from_url", json={
    "article_url": "https://denvergazette.com/aurora/aurora-shooting-thursday/article_2bc2808a-b6dd-11ee-90b9-47213b65f1f5.html",
    "trim": True
})
print(reg.json())

