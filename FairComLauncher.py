#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def launch_latest_edge_server( base_dir ):
    """
    Scans the base directory for FairCom Edge installations, 
    finds the highest version, and launches the server.
    """
    # Regex to match FairCom Edge directories and extract the version number.
    # Example match: FairCom-Edge.windows.64bit.v5.1.5.130
    pattern = re.compile( r"^FairCom-Edge\..*\.v(\d+(?:\.\d+)*)$", re.IGNORECASE )

    highest_version = None
    target_dir = None

    # Scan the directory.
    for entry in os.listdir( base_dir ):
        full_path = os.path.join( base_dir, entry )

        if os.path.isdir( full_path ):
            match = pattern.match( entry )
            if match:
                version_str = match.group( 1 )

                # Convert "5.1.5.130" into (5, 1, 5, 130) for accurate numeric comparison.
                version_tuple = tuple( map( int, version_str.split( '.' ) ) )

                # Update if this is the first found, or if it's a higher version.
                if highest_version is None or version_tuple > highest_version:
                    highest_version = version_tuple
                    target_dir = full_path

    # Launch the server if a matching directory was found.
    if target_dir:
        executable_path = os.path.join( target_dir, "server", "faircom.exe" )
        server_working_dir = os.path.join( target_dir, "server" )

        if os.path.exists( executable_path ):
            version_string = '.'.join( map( str, highest_version ) )
            print( f"Found latest FairCom Edge version: {version_string}" )
            print( f"Launching from: {executable_path}" )

            # Use Popen to launch the server without blocking the script.
            # Setting cwd ensures the server finds its local config files (like ctsrvr.cfg).
            subprocess.Popen( [executable_path], cwd = server_working_dir )
            print( "Server launched successfully." )
        else:
            print( f"Error: Executable not found at expected path: {executable_path}" )
    else:
        print( "Error: No FairCom Edge server directories found in the specified path." )


if __name__ == "__main__":
    # Specify the directory containing your FairCom installations. 
    # Use "." for the current directory, or provide the full absolute path.
    installation_directory = r"C:\Path\To\Your\FairCom\Directory"

    launch_latest_edge_server( installation_directory )
