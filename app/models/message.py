from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime
import math

class Message:
    db='socialsnakes'
    def __init__(self, data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.recipient_id = data['recipient_id']
        self.recipient = data['recipient']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO message (sender_id, recipient_id, text, created_at, updated_at)\
            VALUES (%(sender_id)s, %(recipient_id)s, %(text)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM message WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT u.first_name sender, u2.first_name recipient, m.* FROM user u \
            LEFT JOIN message m ON m.sender_id = u.id \
            LEFT JOIN user u2 ON u2.id = m.recipient_id WHERE u2.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages
            
    def timeDiff(self):
        now = datetime.now()
        diff = now - self.created_at
        if diff.days < 1:
            return f'{math.floor(diff.total_seconds() / 60)} min(s) ago'
        return f'{diff.days} day(s) ago'
        
        
    