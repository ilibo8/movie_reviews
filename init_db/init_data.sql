use movie_reviews;

-- USERS --
insert into users (id, user_name, password, email, is_superuser) values
(null, "superuser", "9fa7b1c3f5ae1bbcd5a9a444acbeba2c0ce3eeecea3508d25964dac2fb29bd64", "superuser@gmail.com", true),
(null, "alex", "d9508122cd143d69df229bf3624b7bcb2b8ac81ed210a0c926455ef119c12abd", "alex@gmail.com", false),
(null, "emma", "52293754fdbea92ab6c69cd64e644deed1552f40ccd3c1cef9d4d63c754d13e3", "emma@gmail.com", false),
(null, "johny", "2b1b370c3baa4ad73cc84d40740834901e691ad9c718246aaa9953da488d99bf", "johny@gmail.com", false),
(null, "sara", "926b4b8a00cfab44b758450fa6bf188d4bf8541c2fd6b3d9b93d152d43a99f64", "sara@gmail.com", false),
(null,  "frida", "02a3ebd48b40ef1f24a1a5716de4417c9b1871d84e9735e9fdaac6613067f8f4", "frida@gmail.com", false),
(null, "nick", "2bf050d4df32457042f9ccf649e2d0c6939a98d63785f0f7483d76d73b9ae201", "nick@gmail.com", false),
(null, "nora", "8579d18ca272b4cb6033ccb8919cb357539ce8726d10f59b5b21d752ea9e8b2a", "nora@gmail.com", false),
(null, "julia", "cdbd41d016cdec10d0ff2291a6bdae398b565a831622bedcd4dcafa69252b5e7", "julia@gmail.com", false),
(null, "simon", "edde0aa0be04ade2ccbb008e7f2f177c7999daf1c3c301b8ced9398ffcae9ef1", "simon@gmail.com", false);

-- GENRES --
insert into genres (name) values
('comedy'),
('romance'),
('action'),
('drama'),
('horror'),
('thriller'),
('western'),
('sci-fi'),
('animation'),
('mystery'),
('biographical'),
('documentary'),
('musical'),
('crime');

-- ACTORS --
insert into actors (id, full_name, nationality) values
(null, 'Jessica Chastain', 'American'),
(null, 'Julia Roberts', 'American'),
(null, 'George Clooney', 'American'),
(null, 'Matt Damon', 'American'),
(null, 'Emily Blunt', 'English'),
(null, 'Morgan Freeman', 'American'),
(null, 'Tim Robbins', 'American'),
(null, 'Tom Hanks', 'American'),
(null, 'Robin Wright', 'American'),
(null, 'John Travolta', 'American'),
(null, 'Bruce Willis', 'American'),
(null, 'Samuel L. Jackson', 'American'),
(null, 'Uma Thurman', 'American'),
(null, 'Carrie-Anne Moss', 'Canadian'),
(null, 'Keanu Reeves', 'Canadian'),
(null, 'Laurence Fishburne', 'American'),
(null, 'Jodie Foster', 'American'),
(null, 'Anthony Hopkins', 'American'),
(null, 'Brad Pitt', 'American');

-- GROUPS --
insert into movie_groups (id, group_name, owner_id, description, date_created) values
(null, "Serbian movies", 5, "For fans of Serbian movies", "2020-01-15"), -- 1
(null, "Romantics", 7, "Best romantic movies", "2019-11-22"), -- 2
(null, "Best funny movies", 3, "We need more laugh", "2020-01-15"), -- 3
(null, "Dramatic", 6, "Who likes drama", "2020-2-10"); -- 4

-- GROUP USERS --
insert into groups_users(group_id, user_id) values
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(2, 3),
(2, 4),
(2, 5),
(2, 7),
(3, 3),
(3, 4),
(3, 5),
(3, 6),
(3, 7),
(3, 8),
(4, 6),
(4, 7),
(4, 2),
(4, 10);


 -- MOVIES --
insert into movies (id, title, director, release_year, country_of_origin) values
(null,'The Shawshank Redemption', 'Frank Darabont', 1994, 'USA'),
(null,'Forrest Gump', 'Robert Zemeckis', 1994, 'USA'),
(null,'Pulp Fiction', 'Quentin Tarantino', 1994, 'USA'),
(null,'The Matrix', 'Lana & Lilly Wachowski', 1999, 'USA'),
(null,'The Silence of the Lambs', 'Jonathan Demme', 1991, 'USA'),
(null,'Se7en', 'David Fincher', 1995, 'USA');

-- MOVIE GENRE --
insert into movie_genre (movie_id, genre_name) values
(1, 'drama'),
(2, 'romance'),
(2, 'drama'),
(3, 'drama'),
(3, 'crime'),
(4, 'action'),
(4, 'sci-fi'),
(5, 'drama'),
(5, 'thriller'),
(5, 'crime'),
(6, 'crime'),
(6, 'drama'),
(6, 'mystery');

-- MOVIE CAST --
insert into movie_cast (movie_id, actor_id) values
(1, 6),
(1, 7),
(2, 8),
(2, 9),
(3, 10),
(3, 11),
(3, 12),
(3, 13),
(4, 14),
(4, 15),
(4, 16),
(5, 17),
(5, 18),
(6, 6),
(6, 19);

insert into recommendations (id, group_user_id, post) values
(null, 5, "My recommendation is Message in a Bottle from 1999 with Kevin Costner and Robin Wright. Just beautiful."),
(null, 6, "Definetly my favourite Original sin with Antonio Banderas and Agelina Jolie."),
(null, 7, "I realy liked Cha Cha Real Smooth, 2022, Dakota Jonson is playing."),
(null, 1, "I watched The Trap (2007), it's not bad."),
(null, 2, "I really liked The Wounds (1998), must watch."),
(null, 3, "Tears for Sale (2008), it's a little bit comedy and fantasy but very good overall."),
(null, 9, "Bad moms 2016, veeery funny"),
(null, 10, "Pitch Perfect 2012, not fan of musicles, but can stop laughing at Rebel Wilson."),
(null, 11, "The Guard 2011, it's not tipical comedy but movie is excellent."),
(null, 12, "The heat 2013, Sandra and Melissa are perfect together."),
(null, 13, "How to be single 2016, also a fan of Rebel."),
(null, 14, "A Million Ways to Die in the West belive it or not Liam is in it,"),
(null, 15, "Girl, Interrupted (1999), with Winona and Angelina, got an Oscar, highly recommend."),
(null, 16, "Pretty Woman (1990), classic, if somebody hasn't seen it."),
(null, 17, "Splendor in the Grass (1961), with Natalie Wood."),
(null, 18, "The Intouchables (2011) french one, excellent.");

insert into reviews (id, movie_id, user_id, rating_number, review) values
(null, 1, 2, 10, "It is no wonder that the film has such a high rating, it is quite literally breathtaking. What can I say that hasn't said before? Not much, it's the story, the acting, the premise, but most of all, this movie is about how it makes you feel. Sometimes you watch a film, and can't remember it days later, this film loves with you, once you've seen it, you don't forget.
The ultimate story of friendship, of hope, and of life, and overcoming adversity.
I understand why so many class this as the best film of all time, it isn't mine, but I get it. If you haven't seen it, or haven't seen it for some time, you need to watch it, it's amazing."),
(null, 1, 3, 10, "This movie is not your ordinary Hollywood flick. It has a great and deep message. This movie has a foundation and just kept on being built on from their and that foundation is hope. Whatever you do, don't listen to the people who say this movie is overrated because this is one of the most inspiring and greatest movies ever. It has everything you could possibly want."),
(null, 1, 4, 10, "I've lost count of the number of times I have seen this movie, but it is more than 20. It has to be one of the best movies ever made. It made me take notice Morgan Freeman and Tim Robbins like I had never noticed any actors before.
I have from a very young age been a huge fan of anything Stephen King writes and had already read the short story that this movie is based on years prior to seeing this movie.
Not everything Stephen King has written that gets turned into a movie comes out well, but this is as close to perfection as it gets and has everything you could ever want in a movie."),
(null, 1, 5, 10, "The Shawshank Redemption has great performances, extremely well written script and story all leading to a deeply emotional climax! One of the best dramas of all time!"),
(null, 1, 6, 9, "Its two stars, Tim Robbins as Andy and Morgan Freeman as Red, are both excellent. Its initial lack of success may have had something to do with its rather clumsy title.
'Shawshank' is not a word that will mean anything to the average person (according to one story Darabont was once asked how his 'rickshaw' film was going) and 'redemption', except in technical legal contexts, normally has a religious connotation. This is not an explicitly religious film; indeed, in its portrayal of Warden Norton as a sanctimonious, Bible-bashing hypocrite, it can be seen as critical of religion.
Nevertheless, the word 'redemption' is perhaps appropriate in this context, after undergoing the hell of Shawshank Andy and Red manage to find a sort of secular redemption. It may be this message of hope that accounts for the film's continuing popularity."),
(null, 2, 6, 10, "'I've made about 20 films and 5 of them are pretty good'-Tom Hanks.
'Forrest Gump' is one of the best movies of all time, guaranteed. I really just love this movie and it has such a special place in my heart. The performances are just so unforgettable and never get out of your head. The characters, I mean the actors turned into them and that's what got to me. The lines are so memorable, touching, and sometimes hilarious."),
(null, 2, 7, 10, "Quite simply, the greatest film ever made.
Humour, sadness, action, drama and a Vietnam film all rolled into one.
But seriously - I bawled my big brown eyes out, on several occasions in this film. A real tear-jerker, and a wonderful character, played to perfection by Tom Hanks. Every bit as worthy for the Oscar as Rooney was to win the Premiership in 2007.
I cannot say it enough: This is THE film of all time. Watch it, and you'll see."),
(null, 2, 8, 10, "The movie has it all too,drama,comedy and it challenges societal norms as well. Then there are the almost endless quotes from the movie that have slipped into everyday speech. They are too numerous to say at this point.One of the toppers for me in the movie is when Forrest is in a quandary about life and wondering as Lt.Dan said we all have a destiny and his Mom says it is where we are all just floating around like a feather in the wind.
Forrest's character terms it very well with this quote,'I think it is a little bit of both.'
From my experiences in life it does appear to be that way. So if you have not seen the movie,see it soon you are in for a real treat. If you did not like it, give it a try again and hopefully you will see it for the great story it is!"),
(null, 2, 9, 10, "I have seen this movie easily a half a dozen times, and I find that the beauty of the film is how Forrest Gump not only shares his innocence and purity with others, including the audience, he also manages to retain that innocence and purity through some very difficult times. As a Viet Nam veteran, and a college graduate of the late Sixties, I could of course personally relate to the various periods that Forrest Gump endures.
I would only mention that the skillful and seamless blending of music, action, and period costume was enthralling. And yet it was so perfectly understated that Forrest Gump's travels through thirty five years of the stormiest and most meaningful years of American history only became clearly defined for the viewer. Even more so than the well known chocolates quote as a metaphor for life, I felt that the remark that stupid is what you do is probably more workable for most of us."),
(null, 2, 10, 10, "Winston Groom's Forrest Gump was a novel that was complicated, but (Oscar winning) director Robert Zemeckis brings events together with visual effects that boggle even George Lucas.
And leading the film in this odyssey of American life is Tom Hanks playing Gump (he won his second Oscar for his portrayal) in a film that shows one man who goes through many events in history to find the one he loves. Well done, well acted, and well directed to pythagorean procision. A++"),
(null, 3, 3, 9, "This is Tarantino's masterpiece, there's no other way to say it. It has arguably one of the smartest scripts I've ever seen. The story, which is non-linear, is so well constructed it takes several viewings to grasp it all. The movie doesn't seem to be about any spesific thing, but there is a subtle hint of redemption as a central theme. The characters and preformances in this movie are practically perfect. This is still one of the best performances I've seen from Sam Jackson, and it's an outrage he didn't win an Oscar. Each scene has its own unique flavour and charm, every segment has its own arc while also tying into the main plot. The comedy is great, the serious moments are great, every word of dialogue is exciting despite seemingly not having any reason to exist. This movie is just such a great time, and I recommend it to everyone who loves movies. I cannot think of a single genuine flaw with it, and it will remain one of my favorite movies for a long time."),
(null, 3, 5, 9, "Before I saw this I assumed it was probably overrated. I was wrong. It lives up to and surpasses its reputation in pretty much every way. I would definitely recommend."),
(null, 3, 7, 9, "Pulp Fiction is the most original, rule breaking film I have ever seen. Instead of following the widely used 3 act structure, Pulp Fiction makes up its own and while the 3 stories may seem completely disconnected at first, once you look closely you can find the underlying themes that they all share. Anyone who says that the movie lacks focus or has no meaning hasn't analysed enough. I highly recommend this film since it is number one on my list of my favourite movies of all time."),
(null, 3, 8, 8, "Just the best movie... I can imagine my family seeing this movie in 30 years. I really love this movie and his soundtrack."),
(null, 4, 3, 9, "When this came out, I was living with a roommate. He went out and saw it, came home and said, 'Dude, you have to go see The Matrix.' So we left and he sat through it a second time. This movie is splendidly done. The mystery about what the Matrix is, unravels and you see a dystopian future unlike any we as a race would want. I have watched this over and over and never tire of it. Everyone does a great job acting in this, the special effects are above par and the story is engaging."),
(null, 4, 4, 10, "This film doesn't age, it will be contemporary even in 2030 or 2040. Wachowski's best one, by far."),
(null, 4, 6, 9, "The film is as well crafted as the matrix itself! On another level entirely to any other science fiction film from the last 20 years . Getting lost in another world, is interly what Cinema is made for. This one takes you into a whole new universe interly "),
(null, 4, 8, 10, "So much greatness about this well done crafty philosophical masterpiece! One of the greatest films ever made; a true benchmark in cinema and huge meticulously brilliant cabinet file of important metaphors. I smile so much while watching The Matrix, I'm so happy it had a 20th anniversary. I'm beyond intrigued by these types of society thought-provoking gems; there aren't enough of them!!"),
(null, 4, 9, 10, "I remember taking a class in social psychology many years ago. The Joy Luck Club figured prominently in the course. I like the idea of combining movies and theory.
I am now studying metaphysics, and any study of reality begins with René Descartes, the father of modern philosophy. Descartes began his intellectual odyssey with this question: How do we know that there is a reality outside our own minds? We each know that we have experiences, and we can be sure of these experiences; therefore, each of us can be sure that we exist. But how do we know that the internal experiences we have corresponds to objects outside our minds?
This is the whole theme of The Matrix. Watching this film is like studying metaphysics."),
(null, 5, 2, 10, "The Silence of the Lambs runs two hours. Anthony Hopkins appears for little more than sixteen minutes, yet during those minutes he hasn't bored you for a second, not even after the tenth or eleventh viewing. Such is the power of his performance, it's absolutely impossible to forget him.His character, Dr.Hannibal 'The Cannibal' Lecter, is a brutal killer with revolting methods and habits, but he's also very intelligent, charismatic and with good taste(you can interpret that as you like).A clichè by now, but who cares? He still is one of the key elements in this wonderful thriller, which sees Jodie Foster's Clarice Starling asking for Lecter's help to catch another killer.The result is a dangerous yet fascinating relationship between the young, unexperienced FBI-agent and the convicted,but basically omnipotent, psychiatrist.He's a step ahead of everyone all the time, and makes sure everyone notices, with his witty, unforgettable one-liners.If there had to be only one reason to worship this movie, then it would have to be the chemistry between the two leading actors.Never before has a non-sexual man/woman connection been more thrilling.Never before has a film's ending been more unsettling and brilliant and left us asking for more."),
(null, 5, 3, 10, "Brilliant Best Picture of 1991 that never gets old. 'The Silence of the Lambs' deals with a young FBI cadet (Oscar-winner Jodie Foster) who is sent to interview a captured madman (Oscar-winner Anthony Hopkins in one of the greatest performances ever on the screen) to find out about a serial killer (Ted Levine) who is stripping the skin from his female victims after they die. The FBI has had no luck with the case and agent Scott Glenn tries to throw a curve-ball to Hopkins by sending Foster. Hopkins is a former doctor of Levine and holds the clues to capturing the unknown criminal. Needless to say the film takes many twists and turns, creating a suspenseful thriller that has no equal. At the heart of 'The Silence of the Lambs' are the confrontations between Hopkins and Foster. They play a complicated chess match of words which results in some of the greatest footage ever captured for the cinema. Hopkins dominates in spite of the fact he has approximately 17 minutes of time in the film. This is a film that will wrap itself around you and you will likely never be able to shake some of the key elements you have seen in this amazing masterpiece. 5 stars out of 5."),
(null, 5, 4, 9, "This is definitely a film that proves you don't need tons of blood and gore to have a good suspense film. Anthony Hopkins performance as the deranged genius Lecter earned him a well deserved Academy Award and the same was true of Jodie Foster's performance as Clarice Starling. This film should go down in history as one of the greatest suspense films in the history of cinema."),
(null, 5, 5, 9, "The Silence of the Lambs, having accomplished the rare feat of winning all five of the major Academy Award categories, is a remarkable achievement in filmmaking. Gruesome, pulpish material was transformed by dedicated participants on all levels of production, and a film that would have failed in the hands of many others wound up becoming a modern masterpiece. Taut direction and a superb screenplay might be the best arguments for the film's power, but the flashiest are certainly delivered in the bravura performances of Hopkins and Foster. Their interplay -- and remember, they only share a handful of scenes together -- is nothing short of riveting."),
(null, 6, 2, 8, "Dark and depressing but just fascinating. Director David Fincher shots the entire film in dim light and shoves the victims mutilated bodies in our face. The grimness of the tone wears you down but that's appropriate considering the subject matter. No humor either. It all leads to a truly harrowing ending. There was supposed to be a happy ending but they (wisely) chose not to do it. Freeman and Pitt work very well together and both give excellent performances. I even thought Paltrow (who I hate) was good! Kevin Spacey is very good too in a small role.
If you have trouble with blood, gore and disturbing subject matter stay far away from this movie. But if you can handle that, watch this one. It's depressing and unpleasant but riveting."),
(null, 6, 4, 7, "Pros: 1. The score is beautifully ominous which only deepens the thrilling and unsettling atmosphere. 2. Brad Pitt (Mills), Morgan Freeman (Somerset), and Kevin Spacey (John Doe) give amazing performances. 3. The colour palette being dark and monotone helps to cement the gloomy and grim tone. 4. The gore and practical effects are immense and they still stand up 25 years later. The sloth, lust, and gluttony murders, in particular, stick in mind. 5. The great cinematography knows when to pull the camera back, as well as to draw it close for great effect. 6. Both Morgan Freeman and Brad Pitt have great chemistry together. 7. The back-and-forth between Somerset, Mills, and John Doe in the police car is one of the most intense and captivating scenes in the history of cinema. 8. The movie presents the interesting and complex moral quandary of: is it immoral to kill the immoral? Even if those immoral people adversely affect other people? And who gets to decide who is immoral, and what punishment should be meted out to them? 9. Despite the underdeveloped character of Tracy (Gwyneth Paltrow), the conclusion is still one of the hardest hitting and iconic endings ever created.
Cons: 1. Tracy is a severely underdeveloped character, with her pregnancy-confessing scene to Somerset feeling lazily forced to add weight to the final scene."),
(null, 6, 6, 8, "A retiring Detective and a young rookie are hunting down a serial killer, a killer with a dark MO, murdering his victims using the seven deadly sins.
As I watch this, it's coming up to its thirtieth anniversary, and it's as fresh now as it was back in 1995, it's an intensely macabre take, crimes that are infinitely macabre and depraved, and intensely twisted.
The combination of Freeman and Pitt is incredible, they work immensely well together, we have the fresh zest of Mills, and the unshakable, but battle weary Somerset. Paltrow and Spacey are excellent in support.
Two hours flashed past, there is no lull, no moment to switch off and boil the kettle, the intensity is immediate, the pacing designed to keep you glued.
I have always thought there is a shade of Alfred Hitchcock about this movie, such is the intelligence of the plot.
Very good visuals, the macabre and gruesome bodies look shocking still, nothing is spared or hidden away."),
(null, 6, 7, 8, "Somerset (Morgan Freeman) is a wearied homicide detective. Mills (Brad Pitt) worked hard to transfer to the troubled precinct. He's married to Tracy (Gwyneth Paltrow). There is a serial killer on the loose delivering his sermon on the Seven Deadly Sins. Somerset is tired of the city. Mills is eager to investigate.
reviewsDirector David Fincher has filled with beautiful darkness. It's more than just the gruesome murders. It's the rain, the music score and the grungy setting. Fincher has weaved together an artistic masterpiece. Freeman is the perfect grizzled veteran. Brad Pitt is a terrific eager newcomer. There are surprising comedy sprinkled in. The final twist is simply cinematic history. The big line is awesome. Pitt delivers it perfectly with so much heart aching pleading. Some do deride its grotesque gloom but that's like complaining about a movie being too funny or too exciting. This is suppose to be dark and it achieves it.");
