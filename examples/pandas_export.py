import pandas as pd
from indianconstitution import get_constitution
ic = get_constitution()
df = pd.DataFrame([a.dict() for a in ic.data.articles])
print(df.head())
