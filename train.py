import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression
import mysql.connector
import os

directory = r'D:/finalhw'
os.makedirs(directory, exist_ok=True)
df = pd.read_csv('train.csv')
df.drop(['POSTED_BY', 'BHK_OR_RK', 'ADDRESS'], axis=1, inplace=True)
df = df.astype(float)
y = df['PRICE_IN_LACS']
X = df.drop(columns=['PRICE_IN_LACS'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1001)

model1 = LinearRegression().fit(X_train, y_train)

new_data = pd.read_csv('test.csv')
new_data.drop(['POSTED_BY', 'BHK_OR_RK', 'ADDRESS'], axis=1, inplace=True)
new_data = new_data.astype(float)
new_data_pred = model1.predict(new_data)
result_df = pd.concat([new_data, pd.DataFrame({'PRICE_IN_LACS': new_data_pred})], axis=1)
result_df.to_excel('D:/finalhw/predicted prices.xlsx', index=False)
print(df.columns)



plt.scatter(y_test, model1.predict(X_test))
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual vs Predicted Prices')
plt.savefig(r'D:/finalhw/static/Actual vs Predicted Prices.png')


plt.hist(new_data_pred, bins=50)
plt.xlabel('Predicted Prices')
plt.ylabel('Frequency')
plt.title('Predicted Prices Distribution')
plt.savefig(r'D:/finalhw/static/Predicted Prices Distribution.png')


# Load the data
result_df = pd.read_excel('D:/finalhw/predicted prices.xlsx')

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = result_df['LONGITUDE']
y = result_df['LATITUDE']
z = result_df['PRICE_IN_LACS']

scatter = ax.scatter(x, y, z, c='b', marker='o')

# Set labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Price (in Lacs)')
ax.set_title('3D Scatter Plot: Latitude vs Longitude vs Price')

# Animation update function
def update(frame):
    ax.view_init(elev=10, azim=frame)  # Rotate the view for each frame

# Create the animation
animation = FuncAnimation(fig, update, frames=range(0, 360, 5), interval=100)

# Save the animation as a looping GIF
animation.save('static/3D_Scatter_Plot_Animation.gif', writer='pillow', fps=5)

# Show the static plot
plt.show()


# Establish the database connection
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test')
cursor = cnx.cursor()

# Create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS predictedcost (
    `UNDER_CONSTRUCTION` VARCHAR(255),
    `RERA` VARCHAR(255),
    `BHK_NO.` VARCHAR(255),
    `SQUARE_FT` VARCHAR(255),
    `READY_TO_MOVE` VARCHAR(255),
    `RESALE` VARCHAR(255),
    `LONGITUDE` VARCHAR(255),
    `LATITUDE` VARCHAR(255),
    `PRICE_IN_LACS` VARCHAR(255)
)
"""
cursor.execute(create_table_query)

# Insert data into the table
for _, row in result_df.iterrows():
    insert_query = "INSERT INTO predictedcost (UNDER_CONSTRUCTION,RERA ,`BHK_NO.` ,SQUARE_FT ,READY_TO_MOVE,RESALE,LONGITUDE ,LATITUDE,PRICE_IN_LACS ) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)"
    values = (row['UNDER_CONSTRUCTION'], row['RERA'],row['BHK_NO.'],row['SQUARE_FT'],row['READY_TO_MOVE'],row['RESALE'],row['LONGITUDE'],row['LATITUDE'],row['PRICE_IN_LACS'])
    cursor.execute(insert_query, values)

# Commit the changes and close the cursor and connection
cnx.commit()
cursor.close()
cnx.close()