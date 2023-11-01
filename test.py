from models.step3_analysis import Step3Analysis
from database.step2_db import Step2DB

if __name__ == "__main__":
    text_to_analyze = """
            How you got involved in the activity? 
            I was attending drawing classes and had recently started to paint on fabric. As my mom’s birthday was close, as a 10-year-old, I could only gift her something that I could make with my hands. I knew she would treasure something that I’ve made myself and took the challenge of painting for her a handkerchief.

            How you went about doing the activity? 
            I had seen a picture of the grandnephews Huey, Dewey, and Louie of Uncle Scrooge (a very popular Disney cartoon). The picture was owned by my classmate. I requested him to give me the image for a few weeks. I sketched the image on the handkerchief carefully. Once I was satisfied, I tightened the canvas using a circular ring. I worked on the afternoons when my mom used to sleep so that she didn’t know anything about it.

            I arranged all the things I would need for the activity, like getting my colors out, washing the palette and keeping it ready, getting water in a bowl for mixing and cleaning, etc. I mixed the colors in the palette to get the desired shade by matching it with the reference image. I colored the big patches first as they were the easiest. I carefully traced the borders with a sharp paint brush using black. It was exhilarating as I would get only about an hour in the afternoon to do this while being hidden. 

            Sometimes, I made a mistake by painting outside the sketched borders and I had to correct it by painting over it with the color meant for the other side. It was frustrating at times, that my brush wasn’t high quality and I would get broken lines. I had to work extra to recolor the broken lines. 

            I diligently worked on this project for about 2 weeks. When everything was ready, I gifted it to my mom on her birthday. I was very happy and satisfied to complete this painting and to get her appreciation.

            What was most satisfying to you about the activity? 
            I liked gifting hand-made items. I was very satisfied that I was able to make something with my hands after putting a lot of effort and gift it to my mom who would treasure it. Even during the activity, I would imagine how happy my mom would feel and that kept me going. Every successful work day that I was hidden was an achievement for me.
        """
    
    db = Step2DB('step_data.db')
    data = db.fetch_data_by_summary_id(33)
    text_to_analyze = data[0][2] + data[0][3] + data[0][4]
    analyzer = Step3Analysis()
    prompt = analyzer.generate_prompt(text_to_analyze)
    response = analyzer.get_response(prompt)

    print(analyzer.usage)

    print(response)

