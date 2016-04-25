import os
nl = os.linesep

import psycopg2


class MissingOutputFileError(Exception):
    pass


class PSQL2PrologConverter(object):
    def __init__(self, db='premierleague', host='localhost', user='postgres',
                 pw='postgres', output_file=None):
        self.db_name = db
        self.db_host = host
        self.db_user = user
        self.db_passwd = pw
        self.output_file = output_file

    @staticmethod
    def write_mode_declarations(outfile):
        w = outfile.write
        w(':- modeh(1,player(+player)).' + nl)
        w(':- modeb(1,team(+team)).' + nl)
        w(':- modeb(1,action(+action)).' + nl)
        # w(':- modeb(1,actionplayer(+action,-player)).' + nl)
        w(':- modeb(1,playerhasaction(+player,-action)).' + nl)
        w(':- modeb(*,actionmatch(+action,-match)).' + nl)
        w(':- modeb(*,actionteam(+action,-team)).' + nl)
        w(':- modeb(1,firstgoal(+action)).' + nl)
        w(':- modeb(1,winninggoal(+action)).' + nl)
        w(':- modeb(1,shotsontargetincgoals(+action,#int)).' + nl)
        w(':- modeb(1,savesmade(+action,#int)).' + nl)
        w(':- modeb(1,timeplayed(+action,#int)).' + nl)
        w(':- modeb(1,starts(+action)).' + nl)
        w(':- modeb(1,substituteon(+action)).' + nl)
        w(':- modeb(1,substituteoff(+action)).' + nl)
        w(':- modeb(1,goals(+action,#int)).' + nl)
        w(':- modeb(1,shotsofftargetincwoodwork(+action,#int)).' + nl)
        w(':- modeb(1,blockedshots(+action,#int)).' + nl)
        w(':- modeb(1,penaltiestaken(+action,#int)).' + nl)
        w(':- modeb(1,penaltygoals(+action,#int)).' + nl)
        w(':- modeb(1,penaltiessaved(+action,#int)).' + nl)
        w(':- modeb(1,penaltiesofftarget(+action,#int)).' + nl)
        w(':- modeb(1,penaltiesnotscored(+action,#int)).' + nl)
        w(':- modeb(1,directfreekickgoals(+action,#int)).' + nl)
        w(':- modeb(1,directfreekickontarget(+action,#int)).' + nl)
        w(':- modeb(1,directfreekickofftarget(+action,#int)).' + nl)
        w(':- modeb(1,blockeddirectfreekick(+action,#int)).' + nl)
        w(':- modeb(1,goalsfrominsidebox(+action,#int)).' + nl)
        w(':- modeb(1,shotsonfrominsidebox(+action,#int)).' + nl)
        w(':- modeb(1,shotsofffrominsidebox(+action,#int)).' + nl)
        w(':- modeb(1,blockedshotsfrominsidebox(+action,#int)).' + nl)
        w(':- modeb(1,goalsfromoutsidebox(+action,#integter)).' + nl)
        w(':- modeb(1,shotsontargetoutsidebox(+action,#int)).' + nl)
        w(':- modeb(1,shotsofftargetoutsidebox(+action,#int)).' + nl)
        w(':- modeb(1,blockedshotsoutsidebox(+action,#int)).' + nl)
        w(':- modeb(1,headedgoals(+action,#int)).' + nl)
        w(':- modeb(1,headedshotsontarget(+action,#int)).' + nl)
        w(':- modeb(1,headedshotsofftarget(+action,#int)).' + nl)
        w(':- modeb(1,headedblockedshots(+action,#int)).' + nl)
        w(':- modeb(1,leftfootgoals(+action,#int)).' + nl)
        w(':- modeb(1,leftfootshotsontarget(+action,#int)).' + nl)
        w(':- modeb(1,leftfootshotsofftarget(+action,#int)).' + nl)
        w(':- modeb(1,leftfootblockedshots(+action,#int)).' + nl)
        w(':- modeb(1,rightfootgoals(+action,#int)).' + nl)
        w(':- modeb(1,rightfootshotsontarget(+action,#int)).' + nl)
        w(':- modeb(1,rightfootshotsofftarget(+action,#int)).' + nl)
        w(':- modeb(1,rightfootblockedshots(+action,#int)).' + nl)
        w(':- modeb(1,othergoals(+action,#int)).' + nl)
        w(':- modeb(1,othershotsontarget(+action,#int)).' + nl)
        w(':- modeb(1,othershotsofftarget(+action,#int)).' + nl)
        w(':- modeb(1,otherblockedshots(+action,#int)).' + nl)
        w(':- modeb(1,shotsclearedoffline(+action,#int)).' + nl)
        w(':- modeb(1,shotsclearedofflineinsidearea(+action,#int)).' + nl)
        w(':- modeb(1,shotsclearedofflineoutsidearea(+action,#int)).' + nl)
        w(':- modeb(1,goalsopenplay(+action,#int)).' + nl)
        w(':- modeb(1,goalsfromcorners(+action,#int)).' + nl)
        w(':- modeb(1,goalsfromthrows(+action,#int)).' + nl)
        w(':- modeb(1,goalsfromdirectfreekick(+action,#int)).' + nl)
        w(':- modeb(1,goalsfromsetplay(+action,#int)).' + nl)
        w(':- modeb(1,goalsfrompenalties(+action,#int)).' + nl)
        w(':- modeb(1,attemptsopenplayontarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromcornersontarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromthrowsontarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromdirectfreekickontarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromsetplayontarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfrompenaltiesontarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsopenplayofftarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromcornersofftarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromthrowsofftarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromdirectfreekickofftarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfromsetplayofftarget(+action,#int)).' + nl)
        w(':- modeb(1,attemptsfrompenaltiesofftarget(+action,#int)).' + nl)
        w(':- modeb(1,goalsasasubstitute(+action,#int)).' + nl)
        w(':- modeb(1,totalsuccessfulpassesall(+action,#int)).' + nl)
        w(':- modeb(1,totalunsuccessfulpassesall(+action,#int)).' + nl)
        w(':- modeb(1,assists(+action,#int)).' + nl)
        w(':- modeb(1,keypasses(+action,#int)).' + nl)
        w(':- modeb(1,totalsuccessfulpassesexclcrossescorners(+action,#int)).'
          + nl)
        w(':- modeb(1,totalunsuccessfulpassesexclcrossescorners('
          '+action,#int)).' + nl)
        w(':- modeb(1,successfulpassesownhalf(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulpassesownhalf(+action,#int)).' + nl)
        w(':- modeb(1,successfulpassesoppositionhalf(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulpassesoppositionhalf(+action,#int)).' + nl)
        w(':- modeb(1,successfulpassesdefensivethird(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulpassesdefensivethird(+action,#int)).' + nl)
        w(':- modeb(1,successfulpassesmiddlethird(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulpassesmiddlethird(+action,#int)).' + nl)
        w(':- modeb(1,successfulpassesfinalthird(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulpassesfinalthird(+action,#int)).' + nl)
        w(':- modeb(1,successfulshortpasses(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulshortpasses(+action,#int)).' + nl)
        w(':- modeb(1,successfullongpasses(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfullongpasses(+action,#int)).' + nl)
        w(':- modeb(1,successfulflickons(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulflickons(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossescorners(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossescorners(+action,#int)).' + nl)
        w(':- modeb(1,cornerstakeninclshortcorners(+action,#int)).' + nl)
        w(':- modeb(1,cornersconceded(+action,#int)).' + nl)
        w(':- modeb(1,successfulcornersintobox(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcornersintobox(+action,#int)).' + nl)
        w(':- modeb(1,shortcorners(+action,#int)).' + nl)
        w(':- modeb(1,throwinstoownplayer(+action,#int)).' + nl)
        w(':- modeb(1,throwinstooppositionplayer(+action,#int)).' + nl)
        w(':- modeb(1,successfuldribbles(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfuldribbles(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossescornersleft(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossescornersleft(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossesleft(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossesleft(+action,#int)).' + nl)
        w(':- modeb(1,successfulcornersleft(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcornersleft(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossescornersright(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossescornersright(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossesright(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossesright(+action,#int)).' + nl)
        w(':- modeb(1,successfulcornersright(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcornersright(+action,#int)).' + nl)
        w(':- modeb(1,successfullongballs(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfullongballs(+action,#int)).' + nl)
        w(':- modeb(1,successfullayoffs(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfullayoffs(+action,#int)).' + nl)
        w(':- modeb(1,throughball(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossescornersintheair(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossescornersintheair(+action,#int)).' + nl)
        w(':- modeb(1,successfulcrossesintheair(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulcrossesintheair(+action,#int)).' + nl)
        w(':- modeb(1,successfulopenplaycrosses(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulopenplaycrosses(+action,#int)).' + nl)
        w(':- modeb(1,touches(+action,#int)).' + nl)
        w(':- modeb(1,goalassistcorner(+action,#int)).' + nl)
        w(':- modeb(1,goalassistfreekick(+action,#int)).' + nl)
        w(':- modeb(1,goalassistthrowin(+action,#int)).' + nl)
        w(':- modeb(1,goalassistgoalkick(+action,#int)).' + nl)
        w(':- modeb(1,goalassistsetpiece(+action,#int)).' + nl)
        w(':- modeb(1,keycorner(+action,#int)).' + nl)
        w(':- modeb(1,keyfreekick(+action,#int)).' + nl)
        w(':- modeb(1,keythrowin(+action,#int)).' + nl)
        w(':- modeb(1,keygoalkick(+action,#int)).' + nl)
        w(':- modeb(1,keysetpieces(+action,#int)).' + nl)
        w(':- modeb(1,duelswon(+action,#int)).' + nl)
        w(':- modeb(1,duelslost(+action,#int)).' + nl)
        w(':- modeb(1,aerialduelswon(+action,#int)).' + nl)
        w(':- modeb(1,aerialduelslost(+action,#int)).' + nl)
        w(':- modeb(1,groundduelswon(+action,#int)).' + nl)
        w(':- modeb(1,groundduelslost(+action,#int)).' + nl)
        w(':- modeb(1,tackleswon(+action,#int)).' + nl)
        w(':- modeb(1,tackleslost(+action,#int)).' + nl)
        w(':- modeb(1,lastmantackle(+action,#int)).' + nl)
        w(':- modeb(1,totalclearances(+action,#int)).' + nl)
        w(':- modeb(1,headedclearances(+action,#int)).' + nl)
        w(':- modeb(1,otherclearances(+action,#int)).' + nl)
        w(':- modeb(1,clearancesofftheline(+action,#int)).' + nl)
        w(':- modeb(1,blocks(+action,#int)).' + nl)
        w(':- modeb(1,interceptions(+action,#int)).' + nl)
        w(':- modeb(1,recoveries(+action,#int)).' + nl)
        w(':- modeb(1,totalfoulsconceded(+action,#int)).' + nl)
        w(':- modeb(1,foulsconcededexchandballspens(+action,#int)).' + nl)
        w(':- modeb(1,totalfoulswon(+action,#int)).' + nl)
        w(':- modeb(1,foulswonindangerareaincpens(+action,#int)).' + nl)
        w(':- modeb(1,foulswonnotindangerarea(+action,#int)).' + nl)
        w(':- modeb(1,foulwonpenalty(+action)).' + nl)
        w(':- modeb(1,handballsconceded(+action,#int)).' + nl)
        w(':- modeb(1,penaltiesconceded(+action,#int)).' + nl)
        w(':- modeb(1,offsides(+action,#int)).' + nl)
        w(':- modeb(1,yellowcards(+action,#int)).' + nl)
        w(':- modeb(1,redcards(+action,#int)).' + nl)
        w(':- modeb(1,goalsconceded(+action,#int)).' + nl)
        w(':- modeb(1,goalsconcededinsidebox(+action,#int)).' + nl)
        w(':- modeb(1,goalsconcededoutsidebox(+action,#int)).' + nl)
        w(':- modeb(1,savesmadefrominsidebox(+action,#int)).' + nl)
        w(':- modeb(1,savesmadefromoutsidebox(+action,#int)).' + nl)
        w(':- modeb(1,savesfrompenalty(+action,#int)).' + nl)
        w(':- modeb(1,catches(+action,#int)).' + nl)
        w(':- modeb(1,punches(+action,#int)).' + nl)
        w(':- modeb(1,drops(+action,#int)).' + nl)
        w(':- modeb(1,crossesnotclaimed(+action,#int)).' + nl)
        w(':- modeb(1,gkdistribution(+action,#int)).' + nl)
        w(':- modeb(1,gksuccessfuldistribution(+action,#int)).' + nl)
        w(':- modeb(1,gkunsuccessfuldistribution(+action,#int)).' + nl)
        w(':- modeb(1,cleansheets(+action,#int)).' + nl)
        w(':- modeb(1,teamcleansheet(+action,#int)).' + nl)
        w(':- modeb(1,errorleadingtogoal(+action,#int)).' + nl)
        w(':- modeb(1,errorleadingtoattempt(+action,#int)).' + nl)
        w(':- modeb(1,challengelost(+action,#int)).' + nl)
        w(':- modeb(1,shotsonconceded(+action,#int)).' + nl)
        w(':- modeb(1,shotsonconcededinsidebox(+action,#int)).' + nl)
        w(':- modeb(1,shotsonconcededoutsidebox(+action,#int)).' + nl)
        w(':- modeb(1,turnovers(+action,#int)).' + nl)
        w(':- modeb(1,dispossessed(+action,#int)).' + nl)
        w(':- modeb(1,bigchances(+action,#int)).' + nl)
        w(':- modeb(1,bigchancesfaced(+action,#int)).' + nl)
        w(':- modeb(1,passforward(+action,#int)).' + nl)
        w(':- modeb(1,passbackward(+action,#int)).' + nl)
        w(':- modeb(1,passleft(+action,#int)).' + nl)
        w(':- modeb(1,passright(+action,#int)).' + nl)
        w(':- modeb(1,unsuccessfulballtouch(+action,#int)).' + nl)
        w(':- modeb(1,successfulballtouch(+action,#int)).' + nl)
        w(':- modeb(1,takeonsoverrun(+action,#int)).' + nl)
        w(':- modeb(1,touchesopenplayfinalthird(+action,#int)).' + nl)
        w(':- modeb(1,touchesopenplayoppbox(+action,#int)).' + nl)
        w(':- modeb(1,touchesopenplayoppsixyards(+action,#int)).' + nl)
        w(':- modeb(1,shot_eff(+action,#float)).' + nl)
        w(':- modeb(1,passes_eff(+action,#float)).' + nl)
        w(':- modeb(1,tackle_eff(+action,#float)).' + nl)
        w(':- modeb(1,dribble_eff(+action,#float)).' + nl)
        w(':- modeb(1,match(+match)).' + nl)
        w(':- modeb(1,teamhome(+match,-team)).' + nl)
        w(':- modeb(1,teamaway(+match,-team)).' + nl)
        w(':- modeb(1,teamhomeformation(+match,-formation)).' + nl)
        w(':- modeb(1,teamawayformation(+match,-formation)).' + nl)
        w(':- modeb(1,resultofteamhome(+match,#int)).' + nl)
        w(':- modeb(1,outcome(+match,-outcome)).' + nl)
        w(':- modeb(1,goalsteamaway(+match,#int)).' + nl)
        w(':- modeb(1,goalsteamhome(+match,#int)).' + nl)
        w(':- modeb(1,scoreraway(+match,-player)).' + nl)
        w(':- modeb(1,scorerhome(+match,-player)).' + nl)
        w(':- modeb(1,formation(+formation)).' + nl)

    @staticmethod
    def convert_players(conn, outfile):
        query = 'SELECT playerid FROM players'
        cursor = conn.cursor()
        cursor.execute(query)

        for player_id in cursor:
            outfile.write('player(player%i).' % player_id + nl)

        cursor.close()

    @staticmethod
    def convert_teams(conn, outfile):
        query = 'SELECT teamid FROM teams'
        cursor = conn.cursor()
        cursor.execute(query)

        for team_id in cursor:
            outfile.write('team(team%i).' % team_id + nl)

        cursor.close()

    @staticmethod
    def convert_actions(conn, outfile):
        query = 'SELECT * FROM actions'
        cursor = conn.cursor()
        cursor.execute(query)

        for res_tuple in cursor:
            playerid, matchid, teamid, firstgoal, winninggoal, \
                shotsontargetincgoals,  savesmade,  timeplayed, positionid, \
                starts, substituteon, substituteoff, goals, \
                shotsofftargetincwoodwork, blockedshots, penaltiestaken, \
                penaltygoals, penaltiessaved, penaltiesofftarget, \
                penaltiesnotscored, directfreekickgoals, \
                directfreekickontarget, directfreekickofftarget, \
                blockeddirectfreekick, goalsfrominsidebox, \
                shotsonfrominsidebox, shotsofffrominsidebox, \
                blockedshotsfrominsidebox, goalsfromoutsidebox, \
                shotsontargetoutsidebox, shotsofftargetoutsidebox, \
                blockedshotsoutsidebox, headedgoals, headedshotsontarget, \
                headedshotsofftarget, headedblockedshots, leftfootgoals, \
                leftfootshotsontarget, leftfootshotsofftarget, \
                leftfootblockedshots, rightfootgoals, rightfootshotsontarget, \
                rightfootshotsofftarget, rightfootblockedshots, othergoals, \
                othershotsontarget, othershotsofftarget, otherblockedshots, \
                shotsclearedoffline, shotsclearedofflineinsidearea, \
                shotsclearedofflineoutsidearea, goalsopenplay, \
                goalsfromcorners, goalsfromthrows, goalsfromdirectfreekick, \
                goalsfromsetplay, goalsfrompenalties, \
                attemptsopenplayontarget, attemptsfromcornersontarget, \
                attemptsfromthrowsontarget, \
                attemptsfromdirectfreekickontarget, \
                attemptsfromsetplayontarget, \
                attemptsfrompenaltiesontarget, attemptsopenplayofftarget, \
                attemptsfromcornersofftarget, attemptsfromthrowsofftarget, \
                attemptsfromdirectfreekickofftarget, \
                attemptsfromsetplayofftarget, attemptsfrompenaltiesofftarget, \
                goalsasasubstitute, totalsuccessfulpassesall, \
                totalunsuccessfulpassesall, assists, keypasses, \
                totalsuccessfulpassesexclcrossescorners, \
                totalunsuccessfulpassesexclcrossescorners, \
                successfulpassesownhalf, unsuccessfulpassesownhalf, \
                successfulpassesoppositionhalf, \
                unsuccessfulpassesoppositionhalf, \
                successfulpassesdefensivethird, \
                unsuccessfulpassesdefensivethird, \
                successfulpassesmiddlethird, unsuccessfulpassesmiddlethird, \
                successfulpassesfinalthird, unsuccessfulpassesfinalthird, \
                successfulshortpasses, unsuccessfulshortpasses, \
                successfullongpasses, unsuccessfullongpasses, \
                successfulflickons, unsuccessfulflickons, \
                successfulcrossescorners, unsuccessfulcrossescorners, \
                cornerstakeninclshortcorners, cornersconceded, \
                successfulcornersintobox, unsuccessfulcornersintobox, \
                shortcorners, throwinstoownplayer, \
                throwinstooppositionplayer, successfuldribbles, \
                unsuccessfuldribbles, successfulcrossescornersleft, \
                unsuccessfulcrossescornersleft, successfulcrossesleft, \
                unsuccessfulcrossesleft, successfulcornersleft, \
                unsuccessfulcornersleft, successfulcrossescornersright, \
                unsuccessfulcrossescornersright, successfulcrossesright, \
                unsuccessfulcrossesright, successfulcornersright, \
                unsuccessfulcornersright, successfullongballs, \
                unsuccessfullongballs, successfullayoffs, \
                unsuccessfullayoffs, throughball, \
                successfulcrossescornersintheair, \
                unsuccessfulcrossescornersintheair, \
                successfulcrossesintheair, unsuccessfulcrossesintheair, \
                successfulopenplaycrosses, unsuccessfulopenplaycrosses, \
                touches, goalassistcorner, goalassistfreekick, \
                goalassistthrowin, goalassistgoalkick, goalassistsetpiece, \
                keycorner, keyfreekick, keythrowin, keygoalkick, \
                keysetpieces, duelswon, duelslost, aerialduelswon, \
                aerialduelslost, groundduelswon, groundduelslost, tackleswon, \
                tackleslost, lastmantackle, totalclearances, \
                headedclearances, otherclearances, clearancesofftheline, \
                blocks, interceptions, recoveries, totalfoulsconceded, \
                foulsconcededexchandballspens, totalfoulswon, \
                foulswonindangerareaincpens, foulswonnotindangerarea, \
                foulwonpenalty, handballsconceded, penaltiesconceded, \
                offsides, yellowcards, redcards, goalsconceded, \
                goalsconcededinsidebox, goalsconcededoutsidebox, \
                savesmadefrominsidebox, savesmadefromoutsidebox, \
                savesfrompenalty, catches, punches, drops, crossesnotclaimed, \
                gkdistribution, gksuccessfuldistribution, \
                gkunsuccessfuldistribution, cleansheets, teamcleansheet, \
                errorleadingtogoal, errorleadingtoattempt, challengelost, \
                shotsonconceded, shotsonconcededinsidebox, \
                shotsonconcededoutsidebox, positioninformation, turnovers, \
                dispossessed, bigchances, bigchancesfaced, passforward, \
                passbackward, passleft, passright, unsuccessfulballtouch, \
                successfulballtouch, takeonsoverrun, \
                touchesopenplayfinalthird, touchesopenplayoppbox, \
                touchesopenplayoppsixyards, team1, team2, shot_eff, \
                passes_eff, tackle_eff, dribble_eff = res_tuple

            action_id = 'action%i%i%i' % (playerid, matchid, teamid)
            outfile.write('action(%s).' % action_id + nl)

            # playerid
            outfile.write('actionplayer(%s,player%i).' % (action_id, playerid)
                          + nl)
            outfile.write('playerhasaction(player%i,%s).' % (playerid, action_id)
                          + nl)
            # matchid
            outfile.write('actionmatch(%s,match%i).' % (action_id, matchid) +
                          nl)
            # teamid
            outfile.write('actionteam(%s,team%i).' % (action_id, teamid) + nl)
            # firstgoal
            if firstgoal == 1:
                outfile.write('firstgoal(%s).' % action_id + nl)
            # winninggoal
            if winninggoal == 1:
                outfile.write('winninggoal(%s).' % action_id + nl)
            # shotsontargetincgoals
            outfile.write('shotsontargetincgoals(%s,%i).' %
                          (action_id, shotsontargetincgoals) + nl)
            # savesmade
            outfile.write('savesmade(%s,%i).' % (action_id, savesmade) + nl)
            # timeplayed
            outfile.write('timeplayed(%s,%i).' % (action_id, timeplayed) + nl)
            # positionid
            # outfile.write('position(%s,position%i' % (action_id, positionid) +
            #               nl)
            # starts
            if starts == 1:
                outfile.write('starts(%s).' % action_id + nl)
            # substituteon
            if substituteon == 1:
                outfile.write('substituteon(%s).' % action_id + nl)
            # substituteoff
            if substituteoff == 1:
                outfile.write('substituteoff(%s).' % action_id + nl)
            # goals
            outfile.write('goals(%s,%i).' % (action_id, goals) + nl)
            # shotsofftargetincwoodwork
            outfile.write('shotsofftargetincwoodwork(%s,%i).' %
                          (action_id, shotsofftargetincwoodwork) + nl)
            # blockedshots
            outfile.write('blockedshots(%s,%i).' % (action_id, blockedshots) +
                          nl)
            # penaltiestaken
            outfile.write('penaltiestaken(%s,%i).' %
                          (action_id, penaltiestaken) + nl)
            # penaltygoals
            outfile.write('penaltygoals(%s,%i).' % (action_id, penaltygoals) +
                          nl)
            # penaltiessaved
            outfile.write('penaltiessaved(%s,%i).' %
                          (action_id, penaltiessaved) + nl)
            # penaltiesofftarget
            outfile.write('penaltiesofftarget(%s,%i).' %
                          (action_id, penaltiesofftarget) + nl)
            # penaltiesnotscored
            outfile.write('penaltiesnotscored(%s,%i).' %
                          (action_id, penaltiesnotscored) + nl)
            # directfreekickgoals
            outfile.write('directfreekickgoals(%s,%i).' %
                          (action_id, directfreekickgoals) + nl)
            # directfreekickontarget
            outfile.write('directfreekickontarget(%s,%i).' %
                          (action_id, directfreekickontarget) + nl)
            # directfreekickofftarget
            outfile.write('directfreekickofftarget(%s,%i).' %
                          (action_id, directfreekickofftarget) + nl)
            # blockeddirectfreekick
            outfile.write('blockeddirectfreekick(%s,%i).' %
                          (action_id, blockeddirectfreekick) + nl)
            # goalsfrominsidebox
            outfile.write('goalsfrominsidebox(%s,%i).' %
                          (action_id, goalsfrominsidebox) + nl)
            # shotsonfrominsidebox
            outfile.write('shotsonfrominsidebox(%s,%i).' %
                          (action_id, shotsonfrominsidebox) + nl)
            # shotsofffrominsidebox
            outfile.write('shotsofffrominsidebox(%s,%i).' %
                          (action_id, shotsofffrominsidebox) + nl)
            # blockedshotsfrominsidebox
            outfile.write('blockedshotsfrominsidebox(%s,%i).' %
                          (action_id, blockedshotsfrominsidebox) + nl)
            # goalsfromoutsidebox
            outfile.write('goalsfromoutsidebox(%s,%i).' %
                          (action_id, goalsfromoutsidebox) + nl)
            # shotsontargetoutsidebox
            outfile.write('shotsontargetoutsidebox(%s,%i).' %
                          (action_id, shotsontargetoutsidebox) + nl)
            # shotsofftargetoutsidebox
            outfile.write('shotsofftargetoutsidebox(%s,%i).' %
                          (action_id, shotsofftargetoutsidebox) + nl)
            # blockedshotsoutsidebox
            outfile.write('blockedshotsoutsidebox(%s,%i).' %
                          (action_id, blockedshotsoutsidebox) + nl)
            # headedgoals
            outfile.write('headedgoals(%s,%i).' % (action_id, headedgoals) + nl)
            # headedshotsontarget
            outfile.write('headedshotsontarget(%s,%i).' %
                          (action_id, headedshotsontarget) + nl)
            # headedshotsofftarget
            outfile.write('headedshotsofftarget(%s,%i).' %
                          (action_id, headedshotsofftarget) + nl)
            # headedblockedshots
            outfile.write('headedblockedshots(%s,%i).' %
                          (action_id, headedblockedshots) + nl)
            # leftfootgoals
            outfile.write('leftfootgoals(%s,%i).' % (action_id, leftfootgoals)
                          + nl)
            # leftfootshotsontarget
            outfile.write('leftfootshotsontarget(%s,%i).' %
                          (action_id, leftfootshotsontarget) + nl)
            # leftfootshotsofftarget
            outfile.write('leftfootshotsofftarget(%s,%i).' %
                          (action_id, leftfootshotsofftarget) + nl)
            # leftfootblockedshots
            outfile.write('leftfootblockedshots(%s,%i).' %
                          (action_id, leftfootblockedshots) + nl)
            # rightfootgoals
            outfile.write('rightfootgoals(%s,%i).' %
                          (action_id, rightfootgoals) + nl)
            # rightfootshotsontarget
            outfile.write('rightfootshotsontarget(%s,%i).' %
                          (action_id, rightfootshotsontarget) + nl)
            # rightfootshotsofftarget
            outfile.write('rightfootshotsofftarget(%s,%i).' %
                          (action_id, rightfootshotsofftarget) + nl)
            # rightfootblockedshots
            outfile.write('rightfootblockedshots(%s,%i).' %
                          (action_id, rightfootblockedshots) + nl)
            # othergoals
            outfile.write('othergoals(%s,%i).' % (action_id, othergoals) + nl)
            # othershotsontarget
            outfile.write('othershotsontarget(%s,%i).' %
                          (action_id, othershotsontarget) + nl)
            # othershotsofftarget
            outfile.write('othershotsofftarget(%s,%i).' %
                          (action_id, othershotsofftarget) + nl)
            # otherblockedshots
            outfile.write('otherblockedshots(%s,%i).' %
                          (action_id, otherblockedshots) + nl)
            # shotsclearedoffline
            outfile.write('shotsclearedoffline(%s,%i).' %
                          (action_id, shotsclearedoffline) + nl)
            # shotsclearedofflineinsidearea
            outfile.write('shotsclearedofflineinsidearea(%s,%i).' %
                          (action_id, shotsclearedofflineinsidearea) + nl)
            # shotsclearedofflineoutsidearea
            outfile.write('shotsclearedofflineoutsidearea(%s,%i).' %
                          (action_id, shotsclearedofflineoutsidearea) + nl)
            # goalsopenplay
            outfile.write('goalsopenplay(%s,%i).' % (action_id, goalsopenplay)
                          + nl)
            # goalsfromcorners
            outfile.write('goalsfromcorners(%s,%i).' %
                          (action_id, goalsfromcorners) + nl)
            # goalsfromthrows
            outfile.write('goalsfromthrows(%s,%i).' %
                          (action_id, goalsfromthrows) + nl)
            # goalsfromdirectfreekick
            outfile.write('goalsfromdirectfreekick(%s,%i).' %
                          (action_id, goalsfromdirectfreekick) + nl)
            # goalsfromsetplay
            outfile.write('goalsfromsetplay(%s,%i).' %
                          (action_id, goalsfromsetplay) + nl)
            # goalsfrompenalties
            outfile.write('goalsfrompenalties(%s,%i).' %
                          (action_id, goalsfrompenalties) + nl)
            # attemptsopenplayontarget
            outfile.write('attemptsopenplayontarget(%s,%i).' %
                          (action_id, attemptsopenplayontarget) + nl)
            # attemptsfromcornersontarget
            outfile.write('attemptsfromcornersontarget(%s,%i).' %
                          (action_id, attemptsfromcornersontarget) + nl)
            # attemptsfromthrowsontarget
            outfile.write('attemptsfromthrowsontarget(%s,%i).' %
                          (action_id, attemptsfromthrowsontarget) + nl)
            # attemptsfromdirectfreekickontarget
            outfile.write('attemptsfromdirectfreekickontarget(%s,%i).' %
                          (action_id, attemptsfromdirectfreekickontarget) + nl)
            # attemptsfromsetplayontarget
            outfile.write('attemptsfromsetplayontarget(%s,%i).' %
                          (action_id, attemptsfromsetplayontarget) + nl)
            # attemptsfrompenaltiesontarget
            outfile.write('attemptsfrompenaltiesontarget(%s,%i).' %
                          (action_id, attemptsfrompenaltiesontarget) + nl)
            # attemptsopenplayofftarget
            outfile.write('attemptsopenplayofftarget(%s,%i).' %
                          (action_id, attemptsopenplayofftarget) + nl)
            # attemptsfromcornersofftarget
            outfile.write('attemptsfromcornersofftarget(%s,%i).' %
                          (action_id, attemptsfromcornersofftarget) + nl)
            # attemptsfromthrowsofftarget
            outfile.write('attemptsfromthrowsofftarget(%s,%i).' %
                          (action_id, attemptsfromthrowsofftarget) + nl)
            # attemptsfromdirectfreekickofftarget
            outfile.write('attemptsfromdirectfreekickofftarget(%s,%i).' %
                          (action_id, attemptsfromdirectfreekickofftarget) + nl)
            # attemptsfromsetplayofftarget
            outfile.write('attemptsfromsetplayofftarget(%s,%i).' %
                          (action_id, attemptsfromsetplayofftarget) + nl)
            # attemptsfrompenaltiesofftarget
            outfile.write('attemptsfrompenaltiesofftarget(%s,%i).' %
                          (action_id, attemptsfrompenaltiesofftarget) + nl)
            # goalsasasubstitute
            outfile.write('goalsasasubstitute(%s,%i).' %
                          (action_id, goalsasasubstitute) + nl)
            # totalsuccessfulpassesall
            outfile.write('totalsuccessfulpassesall(%s,%i).' %
                          (action_id, totalsuccessfulpassesall) + nl)
            # totalunsuccessfulpassesall
            outfile.write('totalunsuccessfulpassesall(%s,%i).' %
                          (action_id, totalunsuccessfulpassesall) + nl)
            # assists
            outfile.write('assists(%s,%i).' % (action_id, assists) + nl)
            # keypasses
            outfile.write('keypasses(%s,%i).' % (action_id, keypasses) + nl)
            # totalsuccessfulpassesexclcrossescorners
            outfile.write('totalsuccessfulpassesexclcrossescorners(%s,%i).' %
                          (action_id, totalsuccessfulpassesexclcrossescorners)
                          + nl)
            # totalunsuccessfulpassesexclcrossescorners
            outfile.write('totalunsuccessfulpassesexclcrossescorners(%s,%i).' %
                          (action_id, totalunsuccessfulpassesexclcrossescorners)
                          + nl)
            # successfulpassesownhalf
            outfile.write('successfulpassesownhalf(%s,%i).' %
                          (action_id, successfulpassesownhalf) + nl)
            # unsuccessfulpassesownhalf
            outfile.write('unsuccessfulpassesownhalf(%s,%i).' %
                          (action_id, unsuccessfulpassesownhalf) + nl)
            # successfulpassesoppositionhalf
            outfile.write('successfulpassesoppositionhalf(%s,%i).' %
                          (action_id, successfulpassesoppositionhalf) + nl)
            # unsuccessfulpassesoppositionhalf
            outfile.write('unsuccessfulpassesoppositionhalf(%s,%i).' %
                          (action_id, unsuccessfulpassesoppositionhalf) + nl)
            # successfulpassesdefensivethird
            outfile.write('successfulpassesdefensivethird(%s,%i).' %
                          (action_id, successfulpassesdefensivethird) + nl)
            # unsuccessfulpassesdefensivethird
            outfile.write('unsuccessfulpassesdefensivethird(%s,%i).' %
                          (action_id, unsuccessfulpassesdefensivethird) + nl)
            # successfulpassesmiddlethird
            outfile.write('successfulpassesmiddlethird(%s,%i).' %
                          (action_id, successfulpassesmiddlethird) + nl)
            # unsuccessfulpassesmiddlethird
            outfile.write('unsuccessfulpassesmiddlethird(%s,%i).' %
                          (action_id, unsuccessfulpassesmiddlethird) + nl)
            # successfulpassesfinalthird
            outfile.write('successfulpassesfinalthird(%s,%i).' %
                          (action_id, successfulpassesfinalthird) + nl)
            # unsuccessfulpassesfinalthird
            outfile.write('unsuccessfulpassesfinalthird(%s,%i).' %
                          (action_id, unsuccessfulpassesfinalthird) + nl)
            # successfulshortpasses
            outfile.write('successfulshortpasses(%s,%i).' %
                          (action_id, successfulshortpasses) + nl)
            # unsuccessfulshortpasses
            outfile.write('unsuccessfulshortpasses(%s,%i).' %
                          (action_id, unsuccessfulshortpasses) + nl)
            # successfullongpasses
            outfile.write('successfullongpasses(%s,%i).' %
                          (action_id, successfullongpasses) + nl)
            # unsuccessfullongpasses
            outfile.write('unsuccessfullongpasses(%s,%i).' %
                          (action_id, unsuccessfullongpasses) + nl)
            # successfulflickons
            outfile.write('successfulflickons(%s,%i).' %
                          (action_id, successfulflickons) + nl)
            # unsuccessfulflickons
            outfile.write('unsuccessfulflickons(%s,%i).' %
                          (action_id, unsuccessfulflickons) + nl)
            # successfulcrossescorners
            outfile.write('successfulcrossescorners(%s,%i).' %
                          (action_id, successfulcrossescorners) + nl)
            # unsuccessfulcrossescorners
            outfile.write('unsuccessfulcrossescorners(%s,%i).' %
                          (action_id, unsuccessfulcrossescorners) + nl)
            # cornerstakeninclshortcorners
            outfile.write('cornerstakeninclshortcorners(%s,%i).' %
                          (action_id, cornerstakeninclshortcorners) + nl)
            # cornersconceded
            outfile.write('cornersconceded(%s,%i).' %
                          (action_id, cornersconceded) + nl)
            # successfulcornersintobox
            outfile.write('successfulcornersintobox(%s,%i).' %
                          (action_id, successfulcornersintobox) + nl)
            # unsuccessfulcornersintobox
            outfile.write('unsuccessfulcornersintobox(%s, %i).' %
                          (action_id, unsuccessfulcornersintobox) + nl)
            # shortcorners
            outfile.write('shortcorners(%s, %i).' %
                          (action_id, shortcorners) + nl)
            # throwinstoownplayer
            outfile.write('throwinstoownplayer(%s,%i).' %
                          (action_id, throwinstoownplayer) + nl)
            # throwinstooppositionplayer
            outfile.write('throwinstooppositionplayer(%s,%i).' %
                          (action_id, throwinstooppositionplayer) + nl)
            # successfuldribbles
            outfile.write('successfuldribbles(%s,%i).' %
                          (action_id, successfuldribbles) + nl)
            # unsuccessfuldribbles
            outfile.write('unsuccessfuldribbles(%s,%i).' %
                          (action_id, unsuccessfuldribbles) + nl)
            # successfulcrossescornersleft
            outfile.write('successfulcrossescornersleft(%s,%i).' %
                          (action_id, successfulcrossescornersleft) + nl)
            # unsuccessfulcrossescornersleft
            outfile.write('unsuccessfulcrossescornersleft(%s,%i).' %
                          (action_id, unsuccessfulcrossescornersleft) + nl)
            # successfulcrossesleft
            outfile.write('successfulcrossesleft(%s,%i).' %
                          (action_id, successfulcrossesleft) + nl)
            # unsuccessfulcrossesleft
            outfile.write('unsuccessfulcrossesleft(%s,%i).' %
                          (action_id, unsuccessfulcrossesleft) + nl)
            # successfulcornersleft
            outfile.write('successfulcornersleft(%s,%i).' %
                          (action_id, successfulcornersleft) + nl)
            # unsuccessfulcornersleft
            outfile.write('unsuccessfulcornersleft(%s,%i).' %
                          (action_id, unsuccessfulcornersleft) + nl)
            # successfulcrossescornersright
            outfile.write('successfulcrossescornersright(%s,%i).' %
                          (action_id, successfulcrossescornersright) + nl)
            # unsuccessfulcrossescornersright
            outfile.write('unsuccessfulcrossescornersright(%s,%i).' %
                          (action_id, unsuccessfulcrossescornersright) + nl)
            # successfulcrossesright
            outfile.write('successfulcrossesright(%s,%i).' %
                          (action_id, successfulcrossesright) + nl)
            # unsuccessfulcrossesright
            outfile.write('unsuccessfulcrossesright(%s,%i).' %
                          (action_id, unsuccessfulcrossesright) + nl)
            # successfulcornersright
            outfile.write('successfulcornersright(%s,%i).' %
                          (action_id, successfulcornersright) + nl)
            # unsuccessfulcornersright
            outfile.write('unsuccessfulcornersright(%s,%i).' %
                          (action_id, unsuccessfulcornersright) + nl)
            # successfullongballs
            outfile.write('successfullongballs(%s,%i).' %
                          (action_id, successfullongballs) + nl)
            # unsuccessfullongballs
            outfile.write('unsuccessfullongballs(%s,%i).' %
                          (action_id, unsuccessfullongballs) + nl)
            # successfullayoffs
            outfile.write('successfullayoffs(%s,%i).' %
                          (action_id, successfullayoffs) + nl)
            # unsuccessfullayoffs
            outfile.write('unsuccessfullayoffs(%s,%i).' %
                          (action_id, unsuccessfullayoffs) + nl)
            # throughball
            outfile.write('throughball(%s,%i).' % (action_id, throughball) + nl)
            # successfulcrossescornersintheair
            outfile.write('successfulcrossescornersintheair(%s,%i).' %
                          (action_id, successfulcrossescornersintheair) + nl)
            # unsuccessfulcrossescornersintheair
            outfile.write('unsuccessfulcrossescornersintheair(%s,%i).' %
                          (action_id, unsuccessfulcrossescornersintheair) + nl)
            # successfulcrossesintheair
            outfile.write('successfulcrossesintheair(%s,%i).' %
                          (action_id, successfulcrossesintheair) + nl)
            # unsuccessfulcrossesintheair
            outfile.write('unsuccessfulcrossesintheair(%s,%i).' %
                          (action_id, unsuccessfulcrossesintheair) + nl)
            # successfulopenplaycrosses
            outfile.write('successfulopenplaycrosses(%s,%i).' %
                          (action_id, successfulopenplaycrosses) + nl)
            # unsuccessfulopenplaycrosses
            outfile.write('unsuccessfulopenplaycrosses(%s,%i).' %
                          (action_id, unsuccessfulopenplaycrosses) + nl)
            # touches
            outfile.write('touches(%s,%i).' % (action_id, touches) + nl)
            # goalassistcorner
            outfile.write('goalassistcorner(%s,%i).' %
                          (action_id, goalassistcorner) + nl)
            # goalassistfreekick
            outfile.write('goalassistfreekick(%s,%i).' %
                          (action_id, goalassistfreekick) + nl)
            # goalassistthrowin
            outfile.write('goalassistthrowin(%s,%i).' %
                          (action_id, goalassistthrowin) + nl)
            # goalassistgoalkick
            outfile.write('goalassistgoalkick(%s,%i).' %
                          (action_id, goalassistgoalkick) + nl)
            # goalassistsetpiece
            outfile.write('goalassistsetpiece(%s,%i).' %
                          (action_id, goalassistsetpiece) + nl)
            # keycorner
            outfile.write('keycorner(%s,%i).' % (action_id, keycorner) + nl)
            # keyfreekick
            outfile.write('keyfreekick(%s,%i).' % (action_id, keyfreekick) + nl)
            # keythrowin
            outfile.write('keythrowin(%s,%i).' % (action_id, keythrowin) + nl)
            # keygoalkick
            outfile.write('keygoalkick(%s,%i).' % (action_id, keygoalkick) + nl)
            # keysetpieces
            outfile.write('keysetpieces(%s,%i).' %
                          (action_id, keysetpieces) + nl)
            # duelswon
            outfile.write('duelswon(%s,%i).' % (action_id, duelswon) + nl)
            # duelslost
            outfile.write('duelslost(%s,%i).' % (action_id, duelslost) + nl)
            # aerialduelswon
            outfile.write('aerialduelswon(%s,%i).' %
                          (action_id, aerialduelswon) + nl)
            # aerialduelslost
            outfile.write('aerialduelslost(%s,%i).' %
                          (action_id, aerialduelslost) + nl)
            # groundduelswon
            outfile.write('groundduelswon(%s,%i).' %
                          (action_id, groundduelswon) + nl)
            # groundduelslost
            outfile.write('groundduelslost(%s,%i).' %
                          (action_id, groundduelslost) + nl)
            # tackleswon
            outfile.write('tackleswon(%s,%i).' % (action_id, tackleswon) + nl)
            # tackleslost
            outfile.write('tackleslost(%s,%i).' % (action_id, tackleslost) + nl)
            # lastmantackle
            outfile.write('lastmantackle(%s,%i).' % (action_id, lastmantackle)
                          + nl)
            # totalclearances
            outfile.write('totalclearances(%s,%i).' %
                          (action_id, totalclearances) + nl)
            # headedclearances
            outfile.write('headedclearances(%s,%i).' %
                          (action_id, headedclearances) + nl)
            # otherclearances
            outfile.write('otherclearances(%s,%i).' %
                          (action_id, otherclearances) + nl)
            # clearancesofftheline
            outfile.write('clearancesofftheline(%s,%i).' %
                          (action_id, clearancesofftheline) + nl)
            # blocks
            outfile.write('blocks(%s,%i).' % (action_id, blocks) + nl)
            # interceptions
            outfile.write('interceptions(%s,%i).' % (action_id, interceptions)
                          + nl)
            # recoveries
            outfile.write('recoveries(%s,%i).' % (action_id, recoveries) + nl)
            # totalfoulsconceded
            outfile.write('totalfoulsconceded(%s,%i).' %
                          (action_id, recoveries) + nl)
            # foulsconcededexchandballspens
            outfile.write('foulsconcededexchandballspens(%s,%i).' %
                          (action_id, foulsconcededexchandballspens) + nl)
            # totalfoulswon
            outfile.write('totalfoulswon(%s,%i).' % (action_id, totalfoulswon)
                          + nl)
            # foulswonindangerareaincpens
            outfile.write('foulswonindangerareaincpens(%s,%i).' %
                          (action_id, foulswonindangerareaincpens) + nl)
            # foulswonnotindangerarea
            outfile.write('foulswonnotindangerarea(%s,%i).' %
                          (action_id, foulswonnotindangerarea) + nl)
            # foulwonpenalty
            outfile.write('foulwonpenalty(%s,%i).' %
                          (action_id, foulwonpenalty) + nl)
            # handballsconceded
            outfile.write('handballsconceded(%s,%i).' %
                          (action_id, handballsconceded) + nl)
            # penaltiesconceded
            outfile.write('penaltiesconceded(%s,%i).' %
                          (action_id, penaltiesconceded) + nl)
            # offsides
            outfile.write('offsides(%s,%i).' % (action_id, offsides) + nl)
            # yellowcards
            outfile.write('yellowcards(%s,%i).' % (action_id, yellowcards) + nl)
            # redcards
            outfile.write('redcards(%s,%i).' % (action_id, redcards) + nl)
            # goalsconceded
            outfile.write('goalsconceded(%s,%i).' %
                          (action_id, goalsconceded) + nl)
            # goalsconcededinsidebox
            outfile.write('goalsconcededinsidebox(%s,%i).' %
                          (action_id, goalsconcededinsidebox) + nl)
            # goalsconcededoutsidebox
            outfile.write('goalsconcededoutsidebox(%s,%i).' %
                          (action_id, goalsconcededoutsidebox) + nl)
            # savesmadefrominsidebox
            outfile.write('savesmadefrominsidebox(%s,%i).' %
                          (action_id, savesmadefrominsidebox) + nl)
            # savesmadefromoutsidebox
            outfile.write('savesmadefromoutsidebox(%s,%i).' %
                          (action_id, savesmadefromoutsidebox) + nl)
            # savesfrompenalty
            outfile.write('savesfrompenalty(%s,%i).' %
                          (action_id, savesfrompenalty) + nl)
            # catches
            outfile.write('catches(%s,%i).' % (action_id, catches) + nl)
            # punches
            outfile.write('punches(%s,%i).' % (action_id, punches) + nl)
            # drops
            outfile.write('drops(%s,%i).' % (action_id, drops) + nl)
            # crossesnotclaimed
            outfile.write('crossesnotclaimed(%s,%i).' %
                          (action_id, crossesnotclaimed) + nl)
            # gkdistribution
            outfile.write('gkdistribution(%s,%i).' %
                          (action_id, gkdistribution) + nl)
            # gksuccessfuldistribution
            outfile.write('gksuccessfuldistribution(%s,%i).' %
                          (action_id, gksuccessfuldistribution) + nl)
            # gkunsuccessfuldistribution
            outfile.write('gkunsuccessfuldistribution(%s,%i).' %
                          (action_id, gkunsuccessfuldistribution) + nl)
            # cleansheets
            if cleansheets == 1:
                outfile.write('cleansheets(%s).' % action_id + nl)
            # teamcleansheet
            if teamcleansheet == 1:
                outfile.write('teamcleansheet(%s).' % action_id + nl)
            # errorleadingtogoal
            outfile.write('errorleadingtogoal(%s,%i).' %
                          (action_id, errorleadingtogoal) + nl)
            # errorleadingtoattempt
            outfile.write('errorleadingtoattempt(%s,%i).' %
                          (action_id, errorleadingtoattempt) + nl)
            # challengelost
            outfile.write('challengelost(%s,%i).' % (action_id, challengelost)
                          + nl)
            # shotsonconceded
            outfile.write('shotsonconceded(%s,%i).' %
                          (action_id, shotsonconceded) + nl)
            # shotsonconcededinsidebox
            outfile.write('shotsonconcededinsidebox(%s,%i).' %
                          (action_id, shotsonconcededinsidebox) + nl)
            # shotsonconcededoutsidebox
            outfile.write('shotsonconcededoutsidebox(%s,%i).' %
                          (action_id, shotsonconcededoutsidebox) + nl)
            # positioninformation
            # outfile.write('positioninformation(%s,positioninformation%i).' %
            #               (action_id, positioninformation) + nl)
            # turnovers
            outfile.write('turnovers(%s,%i).' % (action_id, turnovers) + nl)
            # dispossessed
            outfile.write('dispossessed(%s,%i).' %
                          (action_id, dispossessed) + nl)
            # bigchances
            outfile.write('bigchances(%s,%i).' % (action_id, bigchances) + nl)
            # bigchancesfaced
            outfile.write('bigchancesfaced(%s,%i).' %
                          (action_id, bigchancesfaced) + nl)
            # passforward
            outfile.write('passforward(%s,%i).' % (action_id, passforward) + nl)
            # passbackward
            outfile.write('passbackward(%s,%i).' % (action_id, passbackward) +
                          nl)
            # passleft
            outfile.write('passleft(%s,%i).' % (action_id, passleft) + nl)
            # passright
            outfile.write('passright(%s,%i).' % (action_id, passright) + nl)
            # unsuccessfulballtouch
            outfile.write('unsuccessfulballtouch(%s,%i).' %
                          (action_id, unsuccessfulballtouch) + nl)
            # successfulballtouch
            outfile.write('successfulballtouch(%s,%i).' %
                          (action_id, successfulballtouch) + nl)
            # takeonsoverrun
            outfile.write('takeonsoverrun(%s,%i).' %
                          (action_id, takeonsoverrun) + nl)
            # touchesopenplayfinalthird
            outfile.write('touchesopenplayfinalthird(%s,%i).' %
                          (action_id, touchesopenplayfinalthird) + nl)
            # touchesopenplayoppbox
            outfile.write('touchesopenplayoppbox(%s,%i).' %
                          (action_id, touchesopenplayoppbox) + nl)
            # touchesopenplayoppsixyards
            outfile.write('touchesopenplayoppsixyards(%s,%i).' %
                          (action_id, touchesopenplayoppsixyards) + nl)
            # team1 --> team name --> skipped
            # team2 --> team name --> skipped
            # shot_eff
            outfile.write('shot_eff(%s,%d).' % (action_id, shot_eff) + nl)
            # passes_eff
            outfile.write('passes_eff(%s,%d).' % (action_id, passes_eff) + nl)
            # tackle_eff
            outfile.write('tackle_eff(%s,%d).' % (action_id, tackle_eff) + nl)
            # dribble_eff
            outfile.write('dribble_eff(%s,%d).' % (action_id, dribble_eff) + nl)

        cursor.close()

    @staticmethod
    def convert_matches(conn, outfile):
        query = """
            WITH matchoutcomeclasses AS (
                SELECT -1 AS outcome, 'awayteamwon' AS outcomecls UNION ALL
                SELECT 0 AS outcome, 'draw' AS outcomecls UNION ALL
                SELECT 1 AS outcome, 'hometeamwon' AS outcomecls
            )
            SELECT
                matchid, teamhomeid, teamawayid, teamhomeformation, teamawayformation, resultofteamhome, outcomecls
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
        """
        cursor = conn.cursor()
        cursor.execute(query)

        for res_tuple in cursor:
            matchid, teamhomeid, teamawayid, teamhomeformation, \
                teamawayformation, resultofteamhome, outcomecls = res_tuple

            # matchid
            outfile.write('match(match%i).' % matchid + nl)
            # teamhomeid
            outfile.write('teamhome(match%i,team%i).' % (matchid, teamhomeid) +
                          nl)
            # teamawayid
            outfile.write('teamaway(match%i,team%i).' % (matchid, teamawayid) +
                          nl)
            # teamhomeformation
            outfile.write('teamhomeformation(match%i,formation%i).' %
                          (matchid, teamhomeformation) + nl)
            # teamawayformation
            outfile.write('teamawayformation(match%i,formation%i).' %
                          (matchid, teamawayformation) + nl)
            # resultofteamhome
            outfile.write('resultofteamhome(match%i,%i).' %
                          (matchid, resultofteamhome) + nl)
            # outcomecls
            outfile.write('outcome(match%i,%s).' % (matchid, outcomecls) + nl)
        cursor.close()

    @staticmethod
    def convert_matches_goals_away(conn, outfile):
        query = """
            SELECT
                matches.matchid, sum(actions.goals) AS goals
            FROM
                matches
            JOIN actions ON
                matches.matchid=actions.matchid AND matches.teamawayid=actions.teamid
            GROUP BY
                matches.matchid
        """
        cursor = conn.cursor()
        cursor.execute(query)

        for res_tuple in cursor:
            matchid, goals = res_tuple
            outfile.write('goalsteamaway(match%i,%i).' % (matchid, goals) + nl)
        cursor.close()

    @staticmethod
    def convert_matches_goals_home(conn, outfile):
        query = """
            SELECT
                matches.matchid, sum(actions.goals) AS goals
            FROM
                matches
            JOIN actions ON
                matches.matchid=actions.matchid AND matches.teamhomeid=actions.teamid
            GROUP BY
                matches.matchid
        """
        cursor = conn.cursor()
        cursor.execute(query)

        for res_tuple in cursor:
            matchid, goals = res_tuple
            outfile.write('goalsteamhome(match%i,%i).' % (matchid, goals) + nl)

        cursor.close()

    @staticmethod
    def convert_matches_scorers_away(conn, outfile):
        query = """
            SELECT
                matches.matchid, player_away.playerid AS scorer_away
            FROM
                matches
            JOIN
                actions AS player_away ON
                    (player_away.matchid=matches.matchid AND player_away.teamid=matches.teamawayid)
            WHERE
                goals>0
        """
        cursor = conn.cursor()
        cursor.execute(query)

        for matchid, scorer_away in cursor:
            outfile.write('scoreraway(match%i,player%i).' %
                          (matchid, scorer_away) + nl)
        cursor.close()

    @staticmethod
    def convert_matches_scorers_home(conn, outfile):
        query = """
            SELECT
                matches.matchid, actions.playerid
            FROM
                matches
            JOIN
                actions ON
                    (actions.matchid=matches.matchid AND actions.teamid=matches.teamhomeid)
            WHERE
                goals>0
        """
        cursor = conn.cursor()
        cursor.execute(query)

        for matchid, scorer_home in cursor:
            outfile.write('scorerhome(match%i,player%i).' %
                          (matchid, scorer_home) + nl)
        cursor.close()

    @staticmethod
    def convert_formation(conn, outfile):
        query = """
            (
                SELECT DISTINCT(teamawayformation) AS formationid FROM matches

            ) UNION (
                SELECT DISTINCT(teamhomeformation) FROM matches
            )
        """
        cursor = conn.cursor()
        cursor.execute(query)

        for formation_id in cursor:
            outfile.write('formation(formation%i).' % formation_id + nl)

        cursor.close()

    def convert(self, output_file=None):
        with open(self.output_file, 'w') as out:
            if output_file is not None:
                self.output_file = output_file

            elif self.output_file is None:
                raise MissingOutputFileError()

            conn = psycopg2.connect(database=self.db_name, user=self.db_user,
                                    password=self.db_passwd, host=self.db_host)

            self.write_mode_declarations(out)
            # self.convert_players(conn, out)
            self.convert_actions(conn, out)
            self.convert_matches(conn, out)
            self.convert_matches_goals_away(conn, out)
            self.convert_matches_goals_home(conn, out)
            self.convert_matches_scorers_away(conn, out)
            self.convert_matches_scorers_home(conn, out)
            self.convert_formation(conn, out)

            for outcome_cls in ['awayteamwon', 'hometeamwon', 'draw']:
                out.write('outcome(%s).' % outcome_cls + nl)

            conn.close()
