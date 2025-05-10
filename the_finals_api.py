import pandas as pd
import requests

class TheFinals:
    BASE_URL = "https://api.the-finals-leaderboard.com/v1/leaderboard/"
    PLATFORMS = ["steam", "xbox", "psn"]

    def process_lb_data(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, platform in enumerate(self.PLATFORMS):
            df.insert(i + 6, f"{platform}User", (df[f"{platform}Name"] != '').astype(int))
        df.insert(9, "multiPlatformUser", (df[[f"{p}User" for p in self.PLATFORMS]].sum(axis=1) > 1).astype(int))
        return df

    def request_data(self, url: str, process_lb_data: bool = False, is_ce: bool = False) -> pd.DataFrame:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()["data"]["entries"] if is_ce else response.json()["data"]
            df = pd.DataFrame(data)
            return self.process_lb_data(df) if process_lb_data else df
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch leaderboard data: {e}")

    def request_crossplay_data(self, base_url: str, name: str = "", is_s1: bool = False) -> pd.DataFrame:
        url = f"{base_url}?name={name}" if name else base_url
        dfs = []
        for platform in self.PLATFORMS:
            try:
                response = requests.get(f"{url}{platform}")
                response.raise_for_status()
                dfs.append(pd.DataFrame(response.json()["data"]))
            except requests.RequestException as e:
                raise requests.RequestException(f"Failed to fetch {platform} data: {e}")
        
        full_df = pd.concat(dfs, ignore_index=True)
        for platform in self.PLATFORMS:
            full_df[f"{platform}User"] = 0
        full_df.loc[:10000, "steamUser"] = 1
        full_df.loc[10001:20000, "xboxUser"] = 1
        full_df.loc[20001:30000, "psnUser"] = 1
        
        sort_column = "fame" if is_s1 else "leagueNumber"
        full_df = full_df.sort_values(sort_column, ascending=False).reset_index(drop=True)
        full_df["rank"] = full_df.index + 1
        return full_df

    def get_leaderboard(self, endpoint: str, name: str = "", process_lb_data: bool = False, 
                       is_ce: bool = False, is_crossplay: bool = False, is_s1: bool = False, 
                       type: str = "") -> pd.DataFrame:
        """
        Generic method to fetch leaderboard data from THE FINALS API.
        
        Args:
            endpoint (str): API endpoint (e.g., 'cb1', 's3/crossplay', 'community-event/ce44')
            name (str): Player name to filter leaderboard (optional)
            process_lb_data (bool): Whether to process leaderboard data
            is_ce (bool): Whether this is a community event leaderboard
            is_crossplay (bool): Whether to use crossplay data processing
            is_s1 (bool): Whether to sort by 'fame' (Season 1) instead of 'leagueNumber'
            type (str): Optional leaderboard type (e.g., 'worldtour', 'sponsor')
            
        Returns:
            pd.DataFrame: Leaderboard data
            
        Raises:
            requests.RequestException: If API request fails
        """
        base_url = f"{self.BASE_URL}{endpoint}"
        if type:
            base_url = base_url.replace(endpoint.split('/')[0], f"{endpoint.split('/')[0]}{type}")
        if is_ce:
            base_url = base_url.replace("/leaderboard", "")
        url = f"{base_url}?name={name}" if name else base_url
        
        if is_crossplay:
            return self.request_crossplay_data(base_url, name, is_s1)
        return self.request_data(url, process_lb_data, is_ce)

    def get_cb1_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("cb1", name)

    def get_cb2_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("cb2", name)

    def get_ob_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("ob/crossplay", name)

    def get_s1_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("s1/", name, is_crossplay=True, is_s1=True)

    def get_s2_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("s2/", name, is_crossplay=True)

    def get_s3_lb(self, name: str = "", type: str = "") -> pd.DataFrame:
        return self.get_leaderboard("s3/crossplay", name, type=type)

    def get_s4_lb(self, name: str = "", type: str = "") -> pd.DataFrame:
        return self.get_leaderboard("s4/crossplay", name, type=type)

    def get_s5_lb(self, name: str = "", type: str = "") -> pd.DataFrame:
        return self.get_leaderboard("s5/crossplay", name, type=type)

    def get_s6_lb(self, name: str = "", type: str = "") -> pd.DataFrame:
        return self.get_leaderboard("s6/crossplay", name, type=type)

    def get_the_finals_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("the-finals/crossplay", name, process_lb_data=True)

    def get_the_orf_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("orf/crossplay", name, process_lb_data=True)

    def get_ce44_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("community-event/ce44", name, process_lb_data=True, is_ce=True)
    
    def get_ce48_lb(self, name: str = "") -> pd.DataFrame:
        return self.get_leaderboard("community-event/ce48", name, process_lb_data=True, is_ce=True)
    