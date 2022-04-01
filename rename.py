import os
import pandas as pd
import shutil

def has_subdir(root):
    list_dir = [os.path.isfile(os.path.join('.', f)) for f in os.listdir('.')]
    return all(list_dir)

def add_raw(src_dir, dst_dir ,raw_csv):

    # if not exist, create csv first

    # labels: movie-name (folder name), file-name, filename in raw folder
    try:
        df = pd.read_csv(raw_csv,index_col=0)
    except:
        df = pd.DataFrame(columns=['raw file','movie','source file'])
        df.to_csv(raw_csv)

    # if contains directory apply recursively
    if has_subdir(src_dir):
        raise NotImplemented

    for fname in sorted(os.listdir(src_dir)):
        pth = os.path.join(src_dir,fname)

        # check if file isn't already added
        check = df.loc[df['source file'] == pth]
        if len(check)!=0:
            print('%s already exists in %s' %(pth,dst_dir))
            continue

        # get last index of file
        idx = len(df)
        movie = src_dir.split('/')[-1]

        raw_pth = os.path.join(dst_dir,'raw_%s.png'%str(idx).zfill(5))
        row = {'raw file':raw_pth,'movie':movie,'source file':pth}

        shutil.copyfile(pth,raw_pth)
        df.loc[idx] = [raw_pth,movie,pth]
    df.to_csv(raw_csv)

def rename(src_dir):
    for file in os.listdir(src_dir):
        src_pth = os.path.join(src_dir,file)
        renamed = src_pth.replace('스크린샷','screenshot')
        # import pdb;pdb.set_trace()
        os.rename(src_pth,renamed)
        # import pdb;pdb.set_trace()

if __name__=="__main__":
    movies = ['soul','encanto']

    for mov in movies:
        
        src_dir = './data/face/%s'%mov

        # rename mode
        rename(src_dir)
        continue

        dst_dir = './data/raw/%s'%mov
        
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        # raw_csv = './data/raw.csv'
        # add_raw(src_dir,dst_dir,raw_csv)
        for idx,file in enumerate(sorted(os.listdir(src_dir))):
            src_pth = os.path.join(src_dir,file)
            dst_pth = os.path.join(dst_dir,file)
            shutil.copyfile(src_pth,dst_pth)
            if idx%5==4:
                print('Copied %s to %s'%(src_pth,dst_pth))