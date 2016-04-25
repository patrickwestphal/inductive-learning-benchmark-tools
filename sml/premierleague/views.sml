Prefix xsd:<http://www.w3.org/2001/XMLSchema#>
Prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
Prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#>
Prefix owl:<http://www.w3.org/2002/07/owl#>

Prefix dlo:<http://dl-learner.org/ont/>
Prefix dlr:<http://dl-learner.org/res/>


Create View static As
    Construct {
        dlo:Team a owl:Class .
        dlo:Player a owl:Class .
        dlo:Match a owl:Class .
        dlo:Action a owl:Class .
        dlo:Formation a owl:Class .
        dlo:MatchOutcome a owl:Class .
        dlo:HomeTeamWon rdfs:subClassOf dlo:MatchOutcome .
        dlo:AwayTeamWon rdfs:subClassOf dlo:MatchOutcome .
        dlo:Draw rdfs:subClassOf dlo:MatchOutcome .
        dlo:Position a owl:Class .
        dlr:position6 a dlo:Position .
        dlr:position2 a dlo:Position .
        dlr:position1 a dlo:Position .
        dlr:position4 a dlo:Position .

        dlo:PositionInformation a owl:Class .
        dlr:position_information1 a dlo:PositionInformation .
        dlr:position_information2 a dlo:PositionInformation .
        dlr:position_information3 a dlo:PositionInformation .
        dlr:position_information4 a dlo:PositionInformation .
        dlr:position_information5 a dlo:PositionInformation .
        dlr:position_information6 a dlo:PositionInformation .
        dlr:position_information7 a dlo:PositionInformation .
        dlr:position_information8 a dlo:PositionInformation .
        dlr:position_information9 a dlo:PositionInformation .
        dlr:position_information10 a dlo:PositionInformation .
        dlr:position_information11 a dlo:PositionInformation .
        dlr:position_information12 a dlo:PositionInformation .
        dlr:position_information13 a dlo:PositionInformation .
        dlr:position_information14 a dlo:PositionInformation .
        dlr:position_information15 a dlo:PositionInformation .
        dlr:position_information16 a dlo:PositionInformation .
        dlr:position_information17 a dlo:PositionInformation .
        dlr:position_information18 a dlo:PositionInformation .

        dlo:team_home
            a owl:ObjectProperty ;
            rdfs:domain dlo:Match ;
            rdfs:range dlo:Team .
        dlo:team_away
            a owl:ObjectProperty ;
            rdfs:domain dlo:Match ;
            rdfs:range dlo:Team .
        dlo:match_date
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Match ;
            rdfs:range xsd:date .
        dlo:team_formation
            a owl:ObjectProperty ;
            rdfs:domain dlo:Match ;
            rdfs:range dlo:Formation .
        dlo:team_home_formation rdfs:subPropertyOf dlo:team_formation .
        dlo:team_away_formation rdfs:subPropertyOf dlo:team_formation .
        dlo:match_outcome
            a owl:ObjectProperty ;
            rdfs:domain dlo:Match ;
            rdfs:range dlo:MatchOutcome .
        dlo:scorer
            a owl:ObjectProperty ;
            rdfs:domain dlo:Match ;
            rdfs:range dlo:Player .
        dlo:scorer_home rdfs:subPropertyOf dlo:scorer .
        dlo:scorer_away rdfs:subPropertyOf dlo:scorer .
        dlo:player
            a owl:ObjectProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range dlo:Player .
        dlo:match
            a owl:ObjectProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range dlo:Match .
        dlo:team
            a owl:ObjectPropery ;
            rdfs:domain dlo:Action ;
            rdfs:range dlo:Team .
        dlo:shot_first_goal_in_match
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:shot_winning_goal_in_match 
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:shots_on_target_incl_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_on_target_incl_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:saves_made
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:minutes_played
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:played_on_position
            a owl:ObjectProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range dlo:Position .
        dlo:played_since_start
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:played_since_start
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:was_substituted_on
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:was_substituted_off
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:number_of_goals_shot
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shot_soft_target_incl_woodwork
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:blocked_shots
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:penalties_taken
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:penalty_goals_shot
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:penalties_saved
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:penalties_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:penalties_not_scored
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:direct_free_kicks_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:direct_free_kicks_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:direct_free_kicks_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:blocked_direct_free_kick
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_on_target_from_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_off_target_from_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:blocked_shots_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_on_target_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_off_target_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:blocked_shots_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:headed_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:headed_shots_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:headed_shots_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:headed_blocked_shots
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:left_foot_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:left_foot_shots_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:left_foot_shots_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:left_foot_blocked_shots
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:right_foot_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:right_foot_shots_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:right_foot_shots_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:right_foot_blocked_shots
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:other_goals
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:other_shots_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:other_shots_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:other_blocked_shots
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_cleared_offline
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_cleared_offline_inside_area
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_cleared_offline_outside_area
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_open_play
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_corners
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_throws
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_direct_freekick
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_set_play
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_from_penalties
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_open_play_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_corners_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_throws_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_direct_free_kick_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_set_play_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_penalties_on_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_open_play_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_corners_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_throws_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_direct_free_kick_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_set_play_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:attempts_from_penalties_off_target
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_as_a_substitute
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_successful_passes
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_unsuccessful_passes
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:assists
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:keypasses
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_successful_passes_excl_crosses_corners
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_unsuccessful_passes_excl_crosses_corners
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_passes_in_own_half
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_passes_in_own_half
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_passes_in_opposition_half
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_passes_in_opposition_half
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_passes_in_defensive_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_passes_in_defensive_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_passes_in_middle_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_passes_in_middle_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_passes_in_final_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_passes_in_final_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_short_passes
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_short_passes
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_long_passes
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_long_passes
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_flick_ons
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_flick_ons
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_corners 
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_corners
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:corners_taken_incl_short_corners
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:corners_conceded
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_corners_into_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_corners_into_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:short_corners
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:throw_ins_to_own_player
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:throw_ins_to_opposition_player
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_dribbles
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_dribbles
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_corners_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_corners_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_corners_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_corners_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_corners_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_corners_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_corners_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_corners_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_long_balls
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_long_balls
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_lay_offs
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_lay_offs
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:through_ball
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_corners_int_heair
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_corners_in_the_air
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_crosses_in_the_air
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_crosses_in_the_air
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_open_play_crosses
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_open_play_crosses
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:touches
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goal_assist_corner
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goal_assist_free_kick
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goal_assist_throw_in
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goal_assist_goal_kick
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goal_assist_set_piece
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:key_corner
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:key_free_kick
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:key_throw_in
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:key_goal_kick
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:key_set_pieces
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:duels_won
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:duels_lost
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:aerial_duels_won
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:aerial_duels_lost
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:ground_duels_won
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:ground_duels_lost
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:tackles_won
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:tackles_lost
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:last_man_tackle
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_clearances
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:headed_clearances
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:other_clearances
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:clearances_off_the_line
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:blocks
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:interceptions
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:recoveries
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_fouls_conceded
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:fouls_conceded_excl_handballs_pens
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:total_fouls_won
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:fouls_won_in_danger_area_incl_pens
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:fouls_won_not_in_danger_area
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:foul_won_penalty
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:handballs_conceded
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:penalties_conceded
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:offsides
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:yellow_cards
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:red_cards
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_conceded
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_conceded_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goals_conceded_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:saves_made_from_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:saves_made_from_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:saves_from_penalty
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:catches
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:punches
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:drops
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:crosses_not_claimed
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goalkeeper_distribution
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goalkeeper_successful_distribution
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goalkeeper_unsuccessful_distribution
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:goalkeeper_has_cleansheets
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:team_clean_sheet
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:boolean .
        dlo:error_leading_to_goal
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:error_leading_to_attempt
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:challenge_lost
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_on_target_conceded
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_on_target_conceded_inside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:shots_on_target_conceded_outside_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:position_information
            a owl:ObjectProperty;
            rdfs:domain dlo:Action ;
            rdfs:range dlo:PositionInformation .
        dlo:turnovers
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:dispossessed
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:big_chances
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:big_chances_faced
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:pass_forward
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:pass_backward
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:pass_left
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:pass_right
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:unsuccessful_ball_touch
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:successful_ball_touch
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:take_ons_overrun
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:touches_in_open_play_in_final_third
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:touches_in_open_play_in_opposition_box
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:touches_in_open_play_in_opposition_six_yards
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:nonNegativeInteger .
        dlo:team1
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:string .
        dlo:team2
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:string .
        dlo:shot_efficiency
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:double .
        dlo:passes_efficiency
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:double .
        dlo:tackle_efficiency
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:double .
        dlo:dribble_efficiency
            a owl:DatatypeProperty ;
            rdfs:domain dlo:Action ;
            rdfs:range xsd:double .
        dlo:has_action
            a owl:ObjectProperty ;
            rdfs:domain dlo:Player ;
            rdfs:range dlo:Action .
    }


Create View teams As
    Construct {
        ?team
            a dlo:Team ;
            rdfs:label ?name ;
    }
    With
        ?team = uri(dlr:team, ?teamid)
        ?name = plainLiteral(?name)
    From
        teams
    

Create View players As
    Construct {
        ?player
            a dlo:Player ;
            rdfs:label ?name .
    }
    With
        ?player = uri(dlr:player, ?playerid)
        ?name = plainLiteral(?name)
    From
        players

/*
available teamformation values:
2
3
4
5
6
7
8
10
11
13
17

assuming this somehow encodes the actual team formation, e.g. two in forward
position, 7 in midfield, two in defence and one keeper
*/
Create View formations As
    Construct {
        ?formation a dlo:Formation .
    }
    With
        ?formation = uri(dlr:formation, ?formationid)
    From
        [[
            (
                SELECT DISTINCT(teamawayformation) AS formationid FROM matches
                
            ) UNION (
                SELECT DISTINCT(teamhomeformation) FROM matches
            )

        ]]


Create View matches_scorers_home As
    Construct {
        ?match
            dlo:scorer_home ?scorer .
    }
    With
        ?match = uri(dlr:match, ?matchid)
        ?scorer = uri(dlr:player, ?playerid)
    From
        [[
            SELECT
                matches.matchid, actions.playerid
            FROM
                matches
            JOIN
                actions ON
                    (actions.matchid=matches.matchid AND actions.teamid=matches.teamhomeid)
            WHERE
                goals>0
        ]]


Create View matches_scorers_away As
    Construct {
        ?match
            dlo:scorer_away ?scorer .
    }
    With
        ?match = uri(dlr:match, ?matchid)
        ?scorer = uri(dlr:player, ?scorer_away)
    From
        [[
            SELECT
                matches.matchid, player_away.playerid AS scorer_away
            FROM
                matches
            JOIN
                actions AS player_away ON
                    (player_away.matchid=matches.matchid AND player_away.teamid=matches.teamawayid)
            WHERE
                goals>0
        ]]


Create View matches_goals_home As
    Construct {
        ?match dlo:goals_home ?goals_home .
    }
    With
        ?match = uri(dlr:match, ?matchid)
        ?goals_home = typedLiteral(?sum, xsd:nonNegativeInteger)
    From
        [[
            SELECT
                matches.matchid, sum(actions.goals)
            FROM
                matches
            JOIN actions ON
                matches.matchid=actions.matchid AND matches.teamhomeid=actions.teamid
            GROUP BY
                matches.matchid
        ]]


Create View matches_goals_away As
    Construct {
        ?match dlo:goals_away ?goals_away .
    }
    With
        ?match = uri(dlr:match, ?matchid)
        ?goals_away = typedLiteral(?sum, xsd:nonNegativeInteger)
    From
        [[
            SELECT
                matches.matchid, sum(actions.goals)
            FROM
                matches
            JOIN actions ON
                matches.matchid=actions.matchid AND matches.teamawayid=actions.teamid
            GROUP BY
                matches.matchid
        ]]


Create View matches As
    Construct {
        ?match
                a dlo:Match ;
                rdfs:label ?label ;
                dlo:team_home ?team_home ;
                dlo:team_away ?team_away ;
                dlo:match_date ?date ;
                dlo:team_home_formation ?homeform ;
                dlo:team_away_formation ?awayform ;
                a ?outcomerestr .
        ?outcomerestr
            a owl:Class ;
            a owl:Restriction ;
            owl:onProperty dlo:match_outcome ;
            owl:someValuesFrom ?outcomecls .
    }
    With
        ?match = uri(dlr:match, ?matchid)
        ?label = plainLiteral(concat(?teamhomename, ' : ', ?teamawayname, ' (', ?date, ')'))
        ?team_home = uri(dlr:team, ?teamhomeid)
        ?team_away = uri(dlr:team, ?teamawayid)
        ?date = typedLiteral(?date, xsd:date)
        ?homeform = uri(dlr:formation, ?teamhomeformation)
        ?awayform = uri(dlr:formation, ?teamawayformation)
        ?outcomerestr = bNode(?matchid)
        ?outcomecls = uri(dlo:, ?outcomecls)
    From 
        [[
            WITH matchoutcomeclasses AS (
                SELECT -1 AS outcome, 'AwayTeamWon' AS outcomecls UNION ALL
                SELECT 0 AS outcome, 'Draw' AS outcomecls UNION ALL
                SELECT 1 AS outcome, 'HomeTeamWon' AS outcomecls
            )
            SELECT
                matchid, teamhomeid, teamawayid, teamhomeformation, teamawayformation, resultofteamhome, date, teamhome.name AS teamhomename, teamaway.name AS teamawayname, outcomecls
            FROM
                matches
            LEFT OUTER JOIN
                teams AS teamhome
            ON
                teamhomeid=teamhome.teamid
            LEFT OUTER JOIN
                teams AS teamaway
            ON
                teamawayid=teamaway.teamid
            JOIN
                matchoutcomeclasses
            ON
                resultofteamhome=outcome
        ]]


Create View actions As
    Construct {
        ?action
            a dlo:Action ;
            dlo:player ?player ;
            dlo:match ?match ;
            dlo:team ?team ;
            dlo:shot_first_goal_in_match ?firstgoal ;
            dlo:shot_winning_goal_in_match ?winninggoal ;
            dlo:shots_on_target_incl_goals ?shotsontarget ;
            dlo:saves_made ?savesmade ;
            dlo:minutes_played ?timeplayed ;
            dlo:played_on_position ?positn ;
            dlo:played_since_start ?playedsincestart ;
            dlo:was_substituted_on ?subston ;
            dlo:was_substituted_off ?substoff ;
            dlo:number_of_goals_shot ?goals ;
            dlo:shots_off_target_incl_woodwork ?shotsofftarget ;
            dlo:blocked_shots ?blckdshots ;
            dlo:penalties_taken ?pnlts ;
            dlo:penalty_goals_shot ?pnltygl ;
            dlo:penalties_saved ?pnltiessavd ;
            dlo:penalties_off_target ?pnltiesoff ;
            dlo:penalties_not_scored ?pnltiesnotscored ;
            dlo:direct_free_kicks_goals ?directfreekickgoals ;
            dlo:direct_free_kicks_on_target ?directfreekickontarget ;
            dlo:direct_free_kicks_off_target ?directfreekickofftarget ;
            dlo:blocked_direct_free_kick ?blockeddirectfreekick ;
            dlo:goals_from_inside_box ?goalsfrominsidebox ;
            dlo:shots_on_target_from_inside_box ?shotsonfrominsidebox ;
            dlo:shots_off_target_from_inside_box ?shotsofffrominsidebox ;
            dlo:blocked_shots_inside_box ?blockedshotsfrominsidebox ;
            dlo:goals_from_outside_box ?goalsfromoutsidebox ;
            dlo:shots_on_target_outside_box ?shotsontargetoutsidebox ;
            dlo:shots_off_target_outside_box ?shotsofftargetoutsidebox ;
            dlo:blocked_shots_outside_box ?blockedshotsoutsidebox ;
            dlo:headed_goals ?headedgoals ;
            dlo:headed_shots_on_target ?headedshotsontarget ;
            dlo:headed_shots_off_target ?headedshotsofftarget ;
            dlo:headed_blocked_shots ?headedblockedshots ;
            dlo:left_foot_goals ?leftfootgoals ;
            dlo:left_foot_shots_on_target ?leftfootshotsontarget ;
            dlo:left_foot_shots_off_target ?leftfootshotsofftarget ;
            dlo:left_foot_blocked_shots ?leftfootblockedshots ;
            dlo:right_foot_goals ?rightfootgoals ;
            dlo:right_foot_shots_on_target ?rightfootshotsontarget ;
            dlo:right_foot_shots_off_target ?rightfootshotsofftarget ;
            dlo:right_foot_blocked_shots ?rightfootblockedshots ;
            dlo:other_goals ?othergoals ;
            dlo:other_shots_on_target ?othershotsontarget ;
            dlo:other_shots_off_target ?othershotsofftarget ;
            dlo:other_blocked_shots ?otherblockedshots ;
            dlo:shots_cleared_offline ?shotsclearedoffline ;
            dlo:shots_cleared_offline_inside_area ?shotsclearedofflineinsidearea ;
            dlo:shots_cleared_offline_outside_area ?shotsclearedofflineoutsidearea ;
            dlo:goals_from_open_play ?goalsopenplay ;
            dlo:goals_from_corners ?goalsfromcorners ;
            dlo:goals_from_throws ?goalsfromthrows ;
            dlo:goals_from_direct_freekick ?goalsfromdirectfreekick ;
            dlo:goals_from_set_play ?goalsfromsetplay ;
            dlo:goals_from_penalties ?goalsfrompenalties ;
            dlo:attempts_from_open_play_on_target ?attemptsopenplayontarget ;
            dlo:attempts_from_corners_on_target ?attemptsfromcornersontarget ;
            dlo:attempts_from_throws_on_target ?attemptsfromthrowsontarget ;
            dlo:attempts_from_direct_free_kick_on_target ?attemptsfromdirectfreekickontarget ;
            dlo:attempts_from_set_play_on_target ?attemptsfromsetplayontarget ;
            dlo:attempts_from_penalties_on_target ?attemptsfrompenaltiesontarget ;
            dlo:attempts_from_open_play_off_target ?attemptsopenplayofftarget ;
            dlo:attempts_from_corners_off_target ?attemptsfromcornersofftarget ;
            dlo:attempts_from_throws_off_target ?attemptsfromthrowsofftarget ;
            dlo:attempts_from_direct_free_kick_off_target ?attemptsfromdirectfreekickofftarget ;
            dlo:attempts_from_set_play_off_target ?attemptsfromsetplayofftarget ;
            dlo:attempts_from_penalties_off_target ?attemptsfrompenaltiesofftarget ;
            dlo:goals_as_a_substitute ?goalsasasubstitute ;
            dlo:total_successful_passes ?totalsuccessfulpassesall ;
            dlo:total_unsuccessful_passes ?totalunsuccessfulpassesall ;
            dlo:assists ?assists ;
            dlo:keypasses ?keypasses ;
            dlo:total_successful_passes_excl_crosses_corners ?totalsuccessfulpassesexclcrossescorners ;
            dlo:total_unsuccessful_passes_excl_crosses_corners ?totalunsuccessfulpassesexclcrossescorners ;
            dlo:successful_passes_in_own_half ?successfulpassesownhalf ;
            dlo:unsuccessful_passes_in_own_half ?unsuccessfulpassesownhalf ;
            dlo:successful_passes_in_opposition_half ?successfulpassesoppositionhalf ;
            dlo:unsuccessful_passes_in_opposition_half ?unsuccessfulpassesoppositionhalf ;
            dlo:successful_passes_in_defensive_third ?successfulpassesdefensivethird ;
            dlo:unsuccessful_passes_in_defensive_third ?unsuccessfulpassesdefensivethird ;
            dlo:successful_passes_in_middle_third ?successfulpassesmiddlethird ;
            dlo:unsuccessful_passes_in_middle_third ?unsuccessfulpassesmiddlethird ;
            dlo:successful_passes_in_final_third ?successfulpassesfinalthird ;
            dlo:unsuccessful_passes_in_final_third ?unsuccessfulpassesfinalthird ;
            dlo:successful_short_passes ?successfulshortpasses ;
            dlo:unsuccessful_short_passes ?unsuccessfulshortpasses ;
            dlo:successful_long_passes ?successfullongpasses ;
            dlo:unsuccessful_long_passes ?unsuccessfullongpasses ;
            dlo:successful_flick_ons ?successfulflickons ;
            dlo:unsuccessful_flick_ons ?unsuccessfulflickons ;
            dlo:successful_crosses_corners  ?successfulcrossescorners ;
            dlo:unsuccessful_crosses_corners ?unsuccessfulcrossescorners ;
            dlo:corners_taken_incl_short_corners ?cornerstakeninclshortcorners ;
            dlo:corners_conceded ?cornersconceded ;
            dlo:successful_corners_into_box ?successfulcornersintobox ;
            dlo:unsuccessful_corners_into_box ?unsuccessfulcornersintobox ;
            dlo:short_corners ?shortcorners ;
            dlo:throw_ins_to_own_player ?throwinstoownplayer ;
            dlo:throw_ins_to_opposition_player ?throwinstooppositionplayer ;
            dlo:successful_dribbles ?successfuldribbles ;
            dlo:unsuccessful_dribbles ?unsuccessfuldribbles ;
            dlo:successful_crosses_corners_left ?successfulcrossescornersleft ;
            dlo:unsuccessful_crosses_corners_left ?unsuccessfulcrossescornersleft ;
            dlo:successful_crosses_left ?successfulcrossesleft ;
            dlo:unsuccessful_crosses_left ?unsuccessfulcrossesleft ;
            dlo:successful_corners_left ?successfulcornersleft ;
            dlo:unsuccessful_corners_left ?unsuccessfulcornersleft ;
            dlo:successful_crosses_corners_right ?successfulcrossescornersright ;
            dlo:unsuccessful_crosses_corners_right ?unsuccessfulcrossescornersright ;
            dlo:successful_crosses_right ?successfulcrossesright ;
            dlo:unsuccessful_crosses_right ?unsuccessfulcrossesright ;
            dlo:successful_corners_right ?successfulcornersright ;
            dlo:unsuccessful_corners_right ?unsuccessfulcornersright ;
            dlo:successful_long_balls ?successfullongballs ;
            dlo:unsuccessful_long_balls ?unsuccessfullongballs ;
            dlo:successful_lay_offs ?successfullayoffs ;
            dlo:unsuccessful_lay_offs ?unsuccessfullayoffs ;
            dlo:through_ball ?throughball ;
            dlo:successful_crosses_corners_int_heair ?successfulcrossescornersintheair ;
            dlo:unsuccessful_crosses_corners_in_the_air ?unsuccessfulcrossescornersintheair ;
            dlo:successful_crosses_in_the_air ?successfulcrossesintheair ;
            dlo:unsuccessful_crosses_in_the_air ?unsuccessfulcrossesintheair ;
            dlo:successful_open_play_crosses ?successfulopenplaycrosses ;
            dlo:unsuccessful_open_play_crosses ?unsuccessfulopenplaycrosses ;
            dlo:touches ?touches ;
            dlo:goal_assist_corner ?goalassistcorner ;
            dlo:goal_assist_free_kick ?goalassistfreekick ;
            dlo:goal_assist_throw_in ?goalassistthrowin ;
            dlo:goal_assist_goal_kick ?goalassistgoalkick ;
            dlo:goal_assist_set_piece ?goalassistsetpiece ;
            dlo:key_corner ?keycorner ;
            dlo:key_free_kick ?keyfreekick ;
            dlo:key_throw_in ?keythrowin ;
            dlo:key_goal_kick ?keygoalkick ;
            dlo:key_set_pieces ?keysetpieces ;
            dlo:duels_won ?duelswon ;
            dlo:duels_lost ?duelslost ;
            dlo:aerial_duels_won ?aerialduelswon ;
            dlo:aerial_duels_lost ?aerialduelslost ;
            dlo:ground_duels_won ?groundduelswon ;
            dlo:ground_duels_lost ?groundduelslost ;
            dlo:tackles_won ?tackleswon ;
            dlo:tackles_lost ?tackleslost ;
            dlo:last_man_tackle ?lastmantackle ;
            dlo:total_clearances ?totalclearances ;
            dlo:headed_clearances ?headedclearances ;
            dlo:other_clearances ?otherclearances ;
            dlo:clearances_off_the_line ?clearancesofftheline ;
            dlo:blocks ?blocks ;
            dlo:interceptions ?interceptions ;
            dlo:recoveries ?recoveries ;
            dlo:total_fouls_conceded ?totalfoulsconceded ;
            dlo:fouls_conceded_excl_handballs_pens ?foulsconcededexchandballspens ;
            dlo:total_fouls_won ?totalfoulswon ;
            dlo:fouls_won_in_danger_area_incl_pens ?foulswonindangerareaincpens ;
            dlo:fouls_won_not_in_danger_area ?foulswonnotindangerarea ;
            dlo:foul_won_penalty ?foulwonpenalty ;
            dlo:handballs_conceded ?handballsconceded ;
            dlo:penalties_conceded ?penaltiesconceded ;
            dlo:offsides ?offsides ;
            dlo:yellow_cards ?yellowcards ;
            dlo:red_cards ?redcards ;
            dlo:goals_conceded ?goalsconceded ;
            dlo:goals_conceded_inside_box ?goalsconcededinsidebox ;
            dlo:goals_conceded_outside_box ?goalsconcededoutsidebox ;
            dlo:saves_made_from_inside_box ?savesmadefrominsidebox ;
            dlo:saves_made_from_outside_box ?savesmadefromoutsidebox ;
            dlo:saves_from_penalty ?savesfrompenalty ;
            dlo:catches ?catches ;
            dlo:punches ?punches ;
            dlo:drops ?drops ;
            dlo:crosses_not_claimed ?crossesnotclaimed ;
            dlo:goalkeeper_distribution ?gkdistribution ;
            dlo:goalkeeper_successful_distribution ?gksuccessfuldistribution ;
            dlo:goalkeeper_unsuccessful_distribution ?gkunsuccessfuldistribution ;
            dlo:goalkeeper_has_cleansheets ?cleansheets ;
            dlo:team_clean_sheet ?teamcleansheet ;
            dlo:error_leading_to_goal ?errorleadingtogoal ;
            dlo:error_leading_to_attempt ?errorleadingtoattempt ;
            dlo:challenge_lost ?challengelost ;
            dlo:shots_on_target_conceded ?shotsonconceded ;
            dlo:shots_on_target_conceded_inside_box ?shotsonconcededinsidebox ;
            dlo:shots_on_target_conceded_outside_box ?shotsonconcededoutsidebox ;
            dlo:position_information ?positioninformation ;  // 1-18
            dlo:turnovers ?turnovers ;
            dlo:dispossessed ?dispossessed ;
            dlo:big_chances ?bigchances ;
            dlo:big_chances_faced ?bigchancesfaced ;
            dlo:pass_forward ?passforward ;
            dlo:pass_backward ?passbackward ;
            dlo:pass_left ?passleft ;
            dlo:pass_right ?passright ;
            dlo:unsuccessful_ball_touch ?unsuccessfulballtouch ;
            dlo:successful_ball_touch ?successfulballtouch ;
            dlo:take_ons_overrun ?takeonsoverrun ;
            dlo:touches_in_open_play_in_final_third ?touchesopenplayfinalthird ;
            dlo:touches_in_open_play_in_opposition_box ?touchesopenplayoppbox ;
            dlo:touches_in_open_play_in_opposition_six_yards ?touchesopenplayoppsixyards ;
            dlo:team1 ?team1 ;
            dlo:team2 ?team2 ;
            dlo:shot_efficiency ?shoteff ;
            dlo:passes_efficiency ?passeseff ;
            dlo:tackle_efficiency ?tackleeff ;
            dlo:dribble_efficiency ?dribbleeff .
        ?player dlo:has_action ?action .
    }
    With
        ?action = uri(dlr:action, ?playerid, ?matchid, ?teamid)
        ?player = uri(dlr:player, ?playerid)
        ?match  = uri(dlr:match, ?matchid)
        ?team   = uri(dlr:team, ?teamid)
        ?firstgoal = typedLiteral(?firstgoal, xsd:boolean)
        ?winninggoal = typedLiteral(?winninggoal, xsd:boolean)
        ?shotsontarget = typedLiteral(?shotsontargetincgoals, xsd:nonNegativeInteger)
        ?savesmade = typedLiteral(?savesmade, xsd:nonNegativeInteger)
        ?timeplayed = typedLiteral(?timeplayed, xsd:nonNegativeInteger)
        ?positn = uri(dlr:position, ?positionid)
        ?playedsincestart = typedLiteral(?starts, xsd:boolean)
        ?subston = typedLiteral(?substituteon, xsd:boolean)
        ?substoff = typedLiteral(?substituteoff, xsd:boolean)
        ?goals  = typedLiteral(?goals, xsd:nonNegativeInteger)
        ?shotsofftarget = typedLiteral(?shotsofftargetincwoodwork, xsd:nonNegativeInteger)
        ?blckdshots = typedLiteral(?blockedshots, xsd:nonNegativeInteger)
        ?pnlts  = typedLiteral(?penaltiestaken, xsd:nonNegativeInteger)
        ?pnltygl = typedLiteral(?penaltygoals, xsd:nonNegativeInteger)
        ?pnltiessavd = typedLiteral(?penaltiessaved, xsd:nonNegativeInteger)
        ?pnltiesoff = typedLiteral(?penaltiesofftarget, xsd:nonNegativeInteger)
        ?pnltiesnotscored = typedLiteral(?penaltiesnotscored, xsd:nonNegativeInteger)
        ?directfreekickgoals = typedLiteral(?directfreekickgoals, xsd:nonNegativeInteger)
        ?directfreekickontarget = typedLiteral(?directfreekickontarget, xsd:nonNegativeInteger)
        ?directfreekickofftarget = typedLiteral(?directfreekickofftarget, xsd:nonNegativeInteger)
        ?blockeddirectfreekick = typedLiteral(?blockeddirectfreekick, xsd:nonNegativeInteger)
        ?goalsfrominsidebox = typedLiteral(?goalsfrominsidebox, xsd:nonNegativeInteger)
        ?shotsonfrominsidebox = typedLiteral(?shotsonfrominsidebox, xsd:nonNegativeInteger)
        ?shotsofffrominsidebox = typedLiteral(?shotsofffrominsidebox, xsd:nonNegativeInteger)
        ?blockedshotsfrominsidebox = typedLiteral(?blockedshotsfrominsidebox, xsd:nonNegativeInteger)
        ?goalsfromoutsidebox = typedLiteral(?goalsfromoutsidebox, xsd:nonNegativeInteger)
        ?shotsontargetoutsidebox = typedLiteral(?shotsontargetoutsidebox, xsd:nonNegativeInteger)
        ?shotsofftargetoutsidebox = typedLiteral(?shotsofftargetoutsidebox, xsd:nonNegativeInteger)
        ?blockedshotsoutsidebox = typedLiteral(?blockedshotsoutsidebox, xsd:nonNegativeInteger)
        ?headedgoals = typedLiteral(?headedgoals, xsd:nonNegativeInteger)
        ?headedshotsontarget = typedLiteral(?headedshotsontarget, xsd:nonNegativeInteger)
        ?headedshotsofftarget = typedLiteral(?headedshotsofftarget, xsd:nonNegativeInteger)
        ?headedblockedshots = typedLiteral(?headedblockedshots, xsd:nonNegativeInteger)
        ?leftfootgoals = typedLiteral(?leftfootgoals, xsd:nonNegativeInteger)
        ?leftfootshotsontarget = typedLiteral(?leftfootshotsontarget, xsd:nonNegativeInteger)
        ?leftfootshotsofftarget = typedLiteral(?leftfootshotsofftarget, xsd:nonNegativeInteger)
        ?leftfootblockedshots = typedLiteral(?leftfootblockedshots, xsd:nonNegativeInteger)
        ?rightfootgoals = typedLiteral(?rightfootgoals, xsd:nonNegativeInteger)
        ?rightfootshotsontarget = typedLiteral(?rightfootshotsontarget, xsd:nonNegativeInteger)
        ?rightfootshotsofftarget = typedLiteral(?rightfootshotsofftarget, xsd:nonNegativeInteger)
        ?rightfootblockedshots = typedLiteral(?rightfootblockedshots, xsd:nonNegativeInteger)
        ?othergoals = typedLiteral(?othergoals, xsd:nonNegativeInteger)
        ?othershotsontarget = typedLiteral(?othershotsontarget, xsd:nonNegativeInteger)
        ?othershotsofftarget = typedLiteral(?othershotsofftarget, xsd:nonNegativeInteger)
        ?otherblockedshots = typedLiteral(?otherblockedshots, xsd:nonNegativeInteger)
        ?shotsclearedoffline = typedLiteral(?shotsclearedoffline, xsd:nonNegativeInteger)
        ?shotsclearedofflineinsidearea = typedLiteral(?shotsclearedofflineinsidearea, xsd:nonNegativeInteger)
        ?shotsclearedofflineoutsidearea = typedLiteral(?shotsclearedofflineoutsidearea, xsd:nonNegativeInteger)
        ?goalsopenplay = typedLiteral(?goalsopenplay, xsd:nonNegativeInteger)
        ?goalsfromcorners = typedLiteral(?goalsfromcorners, xsd:nonNegativeInteger)
        ?goalsfromthrows = typedLiteral(?goalsfromthrows, xsd:nonNegativeInteger)
        ?goalsfromdirectfreekick = typedLiteral(?goalsfromdirectfreekick, xsd:nonNegativeInteger)
        ?goalsfromsetplay = typedLiteral(?goalsfromsetplay, xsd:nonNegativeInteger)
        ?goalsfrompenalties = typedLiteral(?goalsfrompenalties, xsd:nonNegativeInteger)
        ?attemptsopenplayontarget = typedLiteral(?attemptsopenplayontarget, xsd:nonNegativeInteger)
        ?attemptsfromcornersontarget = typedLiteral(?attemptsfromcornersontarget, xsd:nonNegativeInteger)
        ?attemptsfromthrowsontarget = typedLiteral(?attemptsfromthrowsontarget, xsd:nonNegativeInteger)
        ?attemptsfromdirectfreekickontarget = typedLiteral(?attemptsfromdirectfreekickontarget, xsd:nonNegativeInteger)
        ?attemptsfromsetplayontarget = typedLiteral(?attemptsfromsetplayontarget, xsd:nonNegativeInteger)
        ?attemptsfrompenaltiesontarget = typedLiteral(?attemptsfrompenaltiesontarget, xsd:nonNegativeInteger)
        ?attemptsopenplayofftarget = typedLiteral(?attemptsopenplayofftarget, xsd:nonNegativeInteger)
        ?attemptsfromcornersofftarget = typedLiteral(?attemptsfromcornersofftarget, xsd:nonNegativeInteger)
        ?attemptsfromthrowsofftarget = typedLiteral(?attemptsfromthrowsofftarget, xsd:nonNegativeInteger)
        ?attemptsfromdirectfreekickofftarget = typedLiteral(?attemptsfromdirectfreekickofftarget, xsd:nonNegativeInteger)
        ?attemptsfromsetplayofftarget = typedLiteral(?attemptsfromsetplayofftarget, xsd:nonNegativeInteger)
        ?attemptsfrompenaltiesofftarget = typedLiteral(?attemptsfrompenaltiesofftarget, xsd:nonNegativeInteger)
        ?goalsasasubstitute = typedLiteral(?goalsasasubstitute, xsd:nonNegativeInteger)
        ?totalsuccessfulpassesall = typedLiteral(?totalsuccessfulpassesall, xsd:nonNegativeInteger)
        ?assists = typedLiteral(?assists, xsd:nonNegativeInteger)
        ?keypasses = typedLiteral(?keypasses, xsd:nonNegativeInteger)
        ?totalsuccessfulpassesexclcrossescorners = typedLiteral(?totalsuccessfulpassesexclcrossescorners, xsd:nonNegativeInteger)
        ?totalunsuccessfulpassesexclcrossescorners = typedLiteral(?totalunsuccessfulpassesexclcrossescorners, xsd:nonNegativeInteger)
        ?successfulpassesownhalf = typedLiteral(?successfulpassesownhalf, xsd:nonNegativeInteger)
        ?unsuccessfulpassesownhalf = typedLiteral(?unsuccessfulpassesownhalf, xsd:nonNegativeInteger)
        ?successfulpassesoppositionhalf = typedLiteral(?successfulpassesoppositionhalf, xsd:nonNegativeInteger)
        ?unsuccessfulpassesoppositionhalf = typedLiteral(?unsuccessfulpassesoppositionhalf, xsd:nonNegativeInteger)
        ?successfulpassesdefensivethird = typedLiteral(?successfulpassesdefensivethird, xsd:nonNegativeInteger)
        ?unsuccessfulpassesdefensivethird = typedLiteral(?unsuccessfulpassesdefensivethird, xsd:nonNegativeInteger)
        ?successfulpassesmiddlethird = typedLiteral(?successfulpassesmiddlethird, xsd:nonNegativeInteger)
        ?unsuccessfulpassesmiddlethird = typedLiteral(?unsuccessfulpassesmiddlethird, xsd:nonNegativeInteger)
        ?successfulpassesfinalthird = typedLiteral(?successfulpassesfinalthird, xsd:nonNegativeInteger)
        ?unsuccessfulpassesfinalthird = typedLiteral(?unsuccessfulpassesfinalthird, xsd:nonNegativeInteger)
        ?successfulshortpasses = typedLiteral(?successfulshortpasses, xsd:nonNegativeInteger)
        ?unsuccessfulshortpasses = typedLiteral(?unsuccessfulshortpasses, xsd:nonNegativeInteger)
        ?successfullongpasses = typedLiteral(?successfullongpasses, xsd:nonNegativeInteger)
        ?unsuccessfullongpasses = typedLiteral(?unsuccessfullongpasses, xsd:nonNegativeInteger)
        ?successfulflickons = typedLiteral(?successfulflickons, xsd:nonNegativeInteger)
        ?unsuccessfulflickons = typedLiteral(?unsuccessfulflickons, xsd:nonNegativeInteger)
        ?successfulcrossescorners = typedLiteral(?successfulcrossescorners, xsd:nonNegativeInteger)
        ?unsuccessfulcrossescorners = typedLiteral(?unsuccessfulcrossescorners, xsd:nonNegativeInteger)
        ?cornerstakeninclshortcorners = typedLiteral(?cornerstakeninclshortcorners, xsd:nonNegativeInteger)
        ?cornersconceded = typedLiteral(?cornersconceded, xsd:nonNegativeInteger)
        ?successfulcornersintobox = typedLiteral(?successfulcornersintobox, xsd:nonNegativeInteger)
        ?unsuccessfulcornersintobox = typedLiteral(?unsuccessfulcornersintobox, xsd:nonNegativeInteger)
        ?shortcorners = typedLiteral(?shortcorners, xsd:nonNegativeInteger)
        ?throwinstoownplayer = typedLiteral(?throwinstoownplayer, xsd:nonNegativeInteger)
        ?throwinstooppositionplayer = typedLiteral(?throwinstooppositionplayer, xsd:nonNegativeInteger)
        ?successfuldribbles = typedLiteral(?successfuldribbles, xsd:nonNegativeInteger)
        ?unsuccessfuldribbles = typedLiteral(?unsuccessfuldribbles, xsd:nonNegativeInteger)
        ?successfulcrossescornersleft = typedLiteral(?successfulcrossescornersleft, xsd:nonNegativeInteger)
        ?unsuccessfulcrossescornersleft = typedLiteral(?unsuccessfulcrossescornersleft, xsd:nonNegativeInteger)
        ?successfulcrossesleft = typedLiteral(?successfulcrossesleft, xsd:nonNegativeInteger)
        ?unsuccessfulcrossesleft = typedLiteral(?unsuccessfulcrossesleft, xsd:nonNegativeInteger)
        ?successfulcornersleft = typedLiteral(?successfulcornersleft, xsd:nonNegativeInteger)
        ?unsuccessfulcornersleft = typedLiteral(?unsuccessfulcornersleft, xsd:nonNegativeInteger)
        ?successfulcrossescornersright = typedLiteral(?successfulcrossescornersright, xsd:nonNegativeInteger)
        ?unsuccessfulcrossescornersright = typedLiteral(?unsuccessfulcrossescornersright, xsd:nonNegativeInteger)
        ?successfulcrossesright = typedLiteral(?successfulcrossesright, xsd:nonNegativeInteger)
        ?unsuccessfulcrossesright = typedLiteral(?unsuccessfulcrossesright, xsd:nonNegativeInteger)
        ?successfulcornersright = typedLiteral(?successfulcornersright, xsd:nonNegativeInteger)
        ?unsuccessfulcornersright = typedLiteral(?unsuccessfulcornersright, xsd:nonNegativeInteger)
        ?successfullongballs = typedLiteral(?successfullongballs, xsd:nonNegativeInteger)
        ?unsuccessfullongballs = typedLiteral(?unsuccessfullongballs, xsd:nonNegativeInteger)
        ?successfullayoffs = typedLiteral(?successfullayoffs, xsd:nonNegativeInteger)
        ?unsuccessfullayoffs = typedLiteral(?unsuccessfullayoffs, xsd:nonNegativeInteger)
        ?throughball = typedLiteral(?throughball, xsd:nonNegativeInteger)
        ?successfulcrossescornersintheair = typedLiteral(?successfulcrossescornersintheair, xsd:nonNegativeInteger)
        ?unsuccessfulcrossescornersintheair = typedLiteral(?unsuccessfulcrossescornersintheair, xsd:nonNegativeInteger)
        ?successfulcrossesintheair = typedLiteral(?successfulcrossesintheair, xsd:nonNegativeInteger)
        ?unsuccessfulcrossesintheair = typedLiteral(?unsuccessfulcrossesintheair, xsd:nonNegativeInteger)
        ?successfulopenplaycrosses = typedLiteral(?successfulopenplaycrosses, xsd:nonNegativeInteger)
        ?unsuccessfulopenplaycrosses = typedLiteral(?unsuccessfulopenplaycrosses, xsd:nonNegativeInteger)
        ?touches = typedLiteral(?touches, xsd:nonNegativeInteger)
        ?goalassistcorner = typedLiteral(?goalassistcorner, xsd:nonNegativeInteger)
        ?goalassistfreekick = typedLiteral(?goalassistfreekick, xsd:nonNegativeInteger)
        ?goalassistthrowin = typedLiteral(?goalassistthrowin, xsd:nonNegativeInteger)
        ?goalassistgoalkick = typedLiteral(?goalassistgoalkick, xsd:nonNegativeInteger)
        ?goalassistsetpiece = typedLiteral(?goalassistsetpiece, xsd:nonNegativeInteger)
        ?keycorner = typedLiteral(?keycorner, xsd:nonNegativeInteger)
        ?keyfreekick = typedLiteral(?keyfreekick, xsd:nonNegativeInteger)
        ?keythrowin = typedLiteral(?keythrowin, xsd:nonNegativeInteger)
        ?keygoalkick = typedLiteral(?keygoalkick, xsd:nonNegativeInteger)
        ?keysetpieces = typedLiteral(?keysetpieces, xsd:nonNegativeInteger)
        ?duelswon = typedLiteral(?duelswon, xsd:nonNegativeInteger)
        ?duelslost = typedLiteral(?duelslost, xsd:nonNegativeInteger)
        ?aerialduelswon = typedLiteral(?aerialduelswon, xsd:nonNegativeInteger)
        ?aerialduelslost = typedLiteral(?aerialduelslost, xsd:nonNegativeInteger)
        ?groundduelswon = typedLiteral(?groundduelswon, xsd:nonNegativeInteger)
        ?groundduelslost = typedLiteral(?groundduelslost, xsd:nonNegativeInteger)
        ?tackleswon = typedLiteral(?tackleswon, xsd:nonNegativeInteger)
        ?tackleslost = typedLiteral(?tackleslost, xsd:nonNegativeInteger)
        ?lastmantackle = typedLiteral(?lastmantackle, xsd:nonNegativeInteger)
        ?totalclearances = typedLiteral(?totalclearances, xsd:nonNegativeInteger)
        ?headedclearances = typedLiteral(?headedclearances, xsd:nonNegativeInteger)
        ?otherclearances = typedLiteral(?otherclearances, xsd:nonNegativeInteger)
        ?clearancesofftheline = typedLiteral(?clearancesofftheline, xsd:nonNegativeInteger)
        ?blocks = typedLiteral(?blocks, xsd:nonNegativeInteger)
        ?interceptions = typedLiteral(?interceptions, xsd:nonNegativeInteger)
        ?recoveries = typedLiteral(?recoveries, xsd:nonNegativeInteger)
        ?totalfoulsconceded = typedLiteral(?totalfoulsconceded, xsd:nonNegativeInteger)
        ?foulsconcededexchandballspens = typedLiteral(?foulsconcededexchandballspens, xsd:nonNegativeInteger)
        ?totalfoulswon = typedLiteral(?totalfoulswon, xsd:nonNegativeInteger)
        ?foulswonindangerareaincpens = typedLiteral(?foulswonindangerareaincpens, xsd:nonNegativeInteger)
        ?foulswonnotindangerarea = typedLiteral(?foulswonnotindangerarea, xsd:nonNegativeInteger)
        ?foulwonpenalty = typedLiteral(?foulwonpenalty, xsd:nonNegativeInteger)
        ?handballsconceded = typedLiteral(?handballsconceded, xsd:nonNegativeInteger)
        ?penaltiesconceded = typedLiteral(?penaltiesconceded, xsd:nonNegativeInteger)
        ?offsides = typedLiteral(?offsides, xsd:nonNegativeInteger)
        ?yellowcards = typedLiteral(?yellowcards, xsd:nonNegativeInteger)
        ?redcards = typedLiteral(?redcards, xsd:nonNegativeInteger)
        ?goalsconceded = typedLiteral(?goalsconceded, xsd:nonNegativeInteger)
        ?goalsconcededinsidebox = typedLiteral(?goalsconcededinsidebox, xsd:nonNegativeInteger)
        ?goalsconcededoutsidebox = typedLiteral(?goalsconcededoutsidebox, xsd:nonNegativeInteger)
        ?savesmadefrominsidebox = typedLiteral(?savesmadefrominsidebox, xsd:nonNegativeInteger)
        ?savesmadefromoutsidebox = typedLiteral(?savesmadefromoutsidebox, xsd:nonNegativeInteger)
        ?savesfrompenalty = typedLiteral(?savesfrompenalty, xsd:nonNegativeInteger)
        ?catches = typedLiteral(?catches, xsd:nonNegativeInteger)
        ?punches = typedLiteral(?punches, xsd:nonNegativeInteger)
        ?drops = typedLiteral(?drops, xsd:nonNegativeInteger)
        ?crossesnotclaimed = typedLiteral(?crossesnotclaimed, xsd:nonNegativeInteger)
        ?gkdistribution = typedLiteral(?gkdistribution, xsd:nonNegativeInteger)
        ?gksuccessfuldistribution = typedLiteral(?gksuccessfuldistribution, xsd:nonNegativeInteger)
        ?gkunsuccessfuldistribution = typedLiteral(?gkunsuccessfuldistribution, xsd:nonNegativeInteger)
        ?cleansheets = typedLiteral(?cleansheets, xsd:boolean)
        ?teamcleansheet = typedLiteral(?teamcleansheet, xsd:boolean)
        ?errorleadingtogoal = typedLiteral(?errorleadingtogoal, xsd:nonNegativeInteger)
        ?errorleadingtoattempt = typedLiteral(?errorleadingtoattempt, xsd:nonNegativeInteger)
        ?challengelost = typedLiteral(?challengelost, xsd:nonNegativeInteger)
        ?shotsonconceded = typedLiteral(?shotsonconceded, xsd:nonNegativeInteger)
        ?shotsonconcededinsidebox = typedLiteral(?shotsonconcededinsidebox, xsd:nonNegativeInteger)
        ?shotsonconcededoutsidebox = typedLiteral(?shotsonconcededoutsidebox, xsd:nonNegativeInteger)
        ?positioninformation = uri(dlr:position_information, ?positioninformation)
        ?turnovers = typedLiteral(?turnovers, xsd:nonNegativeInteger)
        ?dispossessed = typedLiteral(?dispossessed, xsd:nonNegativeInteger)
        ?bigchances = typedLiteral(?bigchances, xsd:nonNegativeInteger)
        ?bigchancesfaced = typedLiteral(?bigchancesfaced, xsd:nonNegativeInteger)
        ?passforward = typedLiteral(?passforward, xsd:nonNegativeInteger)
        ?passbackward = typedLiteral(?passbackward, xsd:nonNegativeInteger)
        ?passleft = typedLiteral(?passleft, xsd:nonNegativeInteger)
        ?passright = typedLiteral(?passright, xsd:nonNegativeInteger)
        ?unsuccessfulballtouch = typedLiteral(?unsuccessfulballtouch, xsd:nonNegativeInteger)
        ?successfulballtouch = typedLiteral(?successfulballtouch, xsd:nonNegativeInteger)
        ?takeonsoverrun = typedLiteral(?takeonsoverrun, xsd:nonNegativeInteger)
        ?touchesopenplayfinalthird = typedLiteral(?touchesopenplayfinalthird, xsd:nonNegativeInteger)
        ?touchesopenplayoppbox = typedLiteral(?touchesopenplayoppbox, xsd:nonNegativeInteger)
        ?touchesopenplayoppsixyards = typedLiteral(?touchesopenplayoppsixyards, xsd:nonNegativeInteger)
        ?team1 = typedLiteral(?team1, xsd:string)
        ?team2 = typedLiteral(?team2, xsd:string)
        ?shoteff = typedLiteral(?shot_eff, xsd:double)
        ?passeseff = typedLiteral(?passes_eff, xsd:double)
        ?tackleeff = typedLiteral(?tackle_eff, xsd:double)
        ?dribbleeff = typedLiteral(?dribble_eff, xsd:double)
        ?totalunsuccessfulpassesall = typedLiteral(?totalunsuccessfulpassesall, xsd:nonNegativeInteger)
    From
        actions

Create View players As
    Construct {
        ?player
            a dlo:Player ;
            rdfs:label ?name
    }
    With
        ?player = uri(dlr:, ?playerid)
        ?name = plainLiteral(?name)
    From
        players

