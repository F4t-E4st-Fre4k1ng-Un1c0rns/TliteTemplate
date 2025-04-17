from src.tlite import Tlite, Message

if __name__ == "__main__":
    
    model = Tlite()
    prompt = [
        Message(
            "Ты Жирировский Владимир Вольфович. Отвечай со свойственными тебе юмором и харизмой",
            "system",
        ),
        Message(
            'Как ты относишься к сербской народной песне "мой дед военные преступник"',
            "user",
        ),
    ]
    print(model.answer(prompt))
    input()
