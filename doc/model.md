1. Templates;
2. Handlers;
 

User.py
    - Register
    - Login
    - Logout

UpdateStatus.py
    - SetLocation
    - UpdateLocation
    - CheckUpdateStatus
    - ClearHasUpdate

MissPerson.py
    - GetPerson
    - get missing person detail and track_list
    - has_find_person    

FindPerson.py
    - Upload_opencv
    - user_upload_image
    - call_for_help

Index.py
    - getStaticPages

2. BuizModels;
    - UserBuizModel:
        - Register
            - unique_check
            - import_missing_person_list
            - register
        - Login
            - identify_check && get_user_info 
        - SetLocation
            - update_to_online
        - UpdateLocation
            - update_to_online
        - Logout
            - delete_to_online
        - CheckUpdateStatus
            - check_update_status
        - ClearHasUpdate
            - set update hasUpdate
    - PersonBuizModel;
        - GetPerson [post list]
            - get_person_list
        - get missing person detail and track_list 
            - get person_detail
            - get track_list [take into two type?]
        - upload_opencv, user_upload_image
            - [2] get_person_detail[check if redis]
                - check info
                - get person_info
                - query missing_person_detail info list through missing_person_id
            - [3] update_person_info
                - update track list
                - update last track date and track_list
                - set update hasUpdate
        - call_for_help
            - add_missing_person
        - has_find_person
            - has_reported
               - can_finish_or_not
            - remove_person_info
                - missing_person_list remove person_id
                - delete track list
                - delete person_id in missing_person_collection 
                - delete track list in track_collection
                - delete_person_from_group[has_find_person]

<!--     - UploadPictureBuizModel;
        - upload_opencv
            - 
        - user_upload_image
        - call_for_help
        - has_find_person -->

    - FaceSetBuizModel
        - upload_opencv, user_upload_image
            - [1] search_person
                - detect
                - search
        - user_upload_image
            - [1] identify_person
                - detect
                - identify
        - create
            - add_missing_person
    - MessageBuizModel
        - upload_opencv, user_upload_image
            - [4]push_message_factory
                - push to somebody
                - push to police
                - push to channel_list
3. CoreModels;
    - UserCoreModel;
        - insert info to user table;[Register]
        - insert missing person list;[Register]
        - check telephone and password;[Login]
        - get missing_person_list through user_id [Login]
        - add to online_collection [SetLocation][todo: update and add can be the same function？]
        - update online_user_collection [UpdateLocation]
        - delete online_user_collection [Logout]
        - get hasUpdate status and through user_id[CheckUpdateStatus]
        - set update hasUpdate[upload_opencv, user_upload_image]
        - check if user online[upload_opencv, user_upload_image]
        - can_finish_or_not[has_find_person]
        - missing_person_list remove person_id.[has_find_person]
    - PersonCoreModel;
        - query missing person by telephone.[Register]
        - query missing person by person list.[GetPerson]
        - query missing_person_detail info list through missing_person_id[get missing person detail and track_list,upload_opencv,user_upload_image]
        - get track_collection by person_id[get missing person detail and track_list,upload_opencv,user_upload_image]
        - update track list[upload_opencv,user_upload_image]
        - update last track date and track_list[upload_opencv,user_upload_image]
        - add_missing_person[call_for_help]
        - delete track list[has_find_person]
        - delete person_id in missing_person_collection [has_find_person]
        - delete track list in track_collection[has_find_person]
    - OSSCoreModel;
        - O[upload_opencv,user_upload_image,call_for_help]
        - get image from key
    - FaceSetCoreModel;
        - detect [upload_opencv, user_upload_image]
        - search [upload_opencv]
        - identify by person_id [user_upload_image]
        - create[call_for_help]
        - delete_person_from_group[has_find_person]
    - LocationCoreModel;
        - get channel_id_list[upload_opencv]
        - 
    - PushCoreModel;
        - push to somebody[upload_opencv,user_upload_image]
        - push to police[upload_opencv,user_upload_image, call_for_help]
        - push to channel_list[upload_opencv,user_upload_image, call_for_help]
    - RedisCoreModel;
        - check info[upload_opencv,user_upload_image]
        - get person_info[upload_opencv]

4. Exception[todo]