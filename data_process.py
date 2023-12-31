import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


# The API endpoint for the POST request
url = "https://v1.cn-abs.com/ajax/ChartMarketHandler.ashx"

# Headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "v1.cn-abs.com",
    "Origin": "https://v1.cn-abs.com",
    "Referer": "https://v1.cn-abs.com/",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

# Payload for the POST request
payload = {    
    'type': 'quarterIssuance' # 最近四年各季度产品发行金额统计
}


def fetch_data(url, headers, data):
    """
    Fetches data from the URL using a POST request.
    
    Args:
        url (str): The URL to which the POST request is made.
        headers (dict): Headers to include in the request.
        data (dict): Data to send in the body of the POST request.
        
    Returns:
        The response from the server.
    """
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        # Assuming the response's content is JSON, parse and return it.
        # If the response is in another format, this line will need to change.
        res = response.json()
        return res
    else:
        print("Failed to retrieve content, status code:", response.status_code)
        return None


def main(data):
    # Fetch and process data from the API
    response = fetch_data(url, headers, data)
    
    if response is not None:
        print("Response from server:", response)
        # Further processing can be done here depending on the structure of response
    return response


def data_parse(data):
    """
    Parses the given data and returns a dictionary containing the parsed information.
    
    Parameters:
        data (list): A list of dictionaries containing the data to be parsed.
        
    Returns:
        dict: A dictionary containing the parsed information. 
    """
    res = {}
    for item in data:
        # print(item)
        q = item['SeriesName']
        # print('q: ', q)
        q_data = []
        points = item['Points']
        # print('points: ', points)
        for point in points:
            year = point['X']
            value = point['Y']
            # print('year: ', year)
            # print('value: ', value)
            q_data.append({'year': year, 'value': value})
        res[q] = q_data
        
    return res


def data2df(data):
    """
    Create a DataFrame from the given data structure and pivot it to have years as the index and quarters as the columns.

    Parameters:
    - data: A dictionary containing the data structure with quarters as keys and a list of records as values. Each record is a dictionary with 'year' and 'value' keys.

    Returns:
    - pivot_df: A pandas DataFrame with years as the index and quarters as the columns, containing the values extracted from the data structure.
    """
    # Flatten the data structure
    flattened_data = []
    for quarter, values in data.items():
        for record in values:
            year = record['year']
            value = record['value']
            flattened_data.append({'Quarter': quarter, 'Year': year, 'Value': value})

    # Create DataFrame from the flattened data
    df = pd.DataFrame(flattened_data)
    # Pivot the DataFrame to have years as the index and quarters as the columns
    pivot_df = df.pivot(index='Year', columns='Quarter', values='Value')
    
    return pivot_df


def save_to_csv(df, fileName):
    """
    Save DataFrame to CSV file.

    Parameters:
    - df (DataFrame): The DataFrame to be saved.

    Returns:
    - None
    """
    # Save DataFrame to CSV file
    df.to_csv('./data/{}.csv'.format(fileName))


def visualization(df):
    """
    Visualizes the data in a line plot.

    Parameters:
    - df: The data to be visualized. It should be a pandas DataFrame.

    Returns:
    None
    """
    # Visualizing the data
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar', figsize=(10, 6)) # Use a bar chart to show each year's quarters side by side
    plt.title('Statistics of the amount of products issued by quarter in the last four years')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend(title='Quarter')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    payload = {    
        'type': 'quarterIssuance' # 最近四年各季度产品发行金额统计
    }
    data = main(data=payload)
    print(data)

    data = data_parse(data)
    print(data)

    df = data2df(data)
    print(df)

    visualization(df)

    file_name = 'quarter_issuance'
    save_to_csv(df, file_name)