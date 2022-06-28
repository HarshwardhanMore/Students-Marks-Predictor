from django.shortcuts import render

import pandas as pd
from app import models

# Create your views here.

def home(request):

    # data = pd.read_csv('../static/dataset.csv')
    data = pd.read_csv('static/dataset.csv')
    
    x = data[['number_courses','time_study']]
    y = data['Marks']

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(x_train,y_train)
    y_predict = model.predict(x_test)

    # print(y_predict[0:5])
    # print(y_test.head(5))

    # print(model.score(x_train,y_train))
    
    
    # --------------------------------------------------------------------------
    
    
    student_data_object = models.Student_Data()

    predicted_output = ['Waiting...']

    if request.method == 'POST':
        
        student_data_object.courses = request.POST.get('courses')
        student_data_object.time = float(request.POST.get('time'))

        new_row = {
            'number_courses':student_data_object.courses, 
            'time_study':student_data_object.time
        }

        data = data.append(new_row,ignore_index=True)
        # new_row = data.iloc[-1].values[:2].reshape(2,1)

        # print(data.tail(1))
        # print(type((data.tail(1)).iloc[0,1]))
        predicted_output = model.predict(data.tail(1).drop('Marks',axis=1))
        # print(predicted_output)

        student_data_object.marks = predicted_output

        data.iloc[-1,2] = predicted_output[0]
        # print(data.iloc[-1,2])

    return render( request, 'home.html',{ 'marks': round(predicted_output[0],3) } )
