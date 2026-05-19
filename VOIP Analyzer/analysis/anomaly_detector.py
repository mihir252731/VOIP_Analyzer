from sklearn.ensemble import IsolationForest

def detect_anomalies(features):
    clf = IsolationForest(contamination=0.1)
    clf.fit(features)
    predictions = clf.predict(features)
    return predictions
