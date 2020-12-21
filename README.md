Please use tag v4.0

Usage:

    $ git clone https://github.com/knaw0128/Mr.Crazy_Dog
    $ cd Mr.Crazy_Dog
    $ python3 arena.py --agent1=base_agent.MyAgent_knaw --agent2=base_agent.RandomAgent

### Team members
    - Team leader:
        - name: Wei-Tung
        - student_id: b09902063
        - github: [knaw0128](https://github.com/knaw0128)
    - member:
        - name: Kai-Feng
        - student_id: b09902060	
        - github: [Tobbys1523](https://github.com/Tobbys1523)

Report:

     We choose to evaluate each point with its position 
     The 4 corners hold the highest piority, while the points around it hold the lowest one.
     The points on the edge hold the second piority and the others hold the third one.
     Our agent will pick the point with priority as high as possible.
     If more than one points hold the same priority, the agent will compare those steps,
     with which cause the opponent have the least legal moves after two steps.
     When it comes to the last 7 moves before the game ends, our agent starts to choose the move
     that can flip the most pieces of the opponent.
