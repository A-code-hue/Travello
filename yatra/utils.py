# yatra/utils.py
import pandas as pd

# Mock data for demonstration (this would typically come from a database or CSV file)
data = pd.DataFrame({
    'name': ['Bahubali Jharana', 'Mustang', 'Pokhara', 'Lumbini', 'Sukute Beach', 'Kathmandu', 'Janakpur', 'Kadadevi-Sailung', 'Bhotekoshi-Rafting', 'Chitlang', 'Khotang Halesi', 'Trisuli' ],
    'days': [3, 6, 3, 3, 3, 5,3,4,2,3,4,3 ],
    'desc': ['Adventure, Nature, Escape', 'Spiritual, Scenic, Adventure', 'Scenic, Adventure', 'Historic Places', 'Beach, Adventure', 'Spiritual, Meditation', 'Family, Historic Places','Scenic, Adventure', 'Rafting, Adventure', 'Escape, Nature', 'Spiritual, Scenic, Adventure', 'Adventure, Nature, Escape'],
    'price': [3600, 39000, 29900, 20000, 3900, 27900, 25000, 30000, 3500, 3600, 35000, 3500 ]
})

def recommend_tours(preference):
    # Basic recommendation logic based on the description containing the preference
    recommended = data[data['desc'].str.contains(preference, case=False, na=False)]
    return recommended
