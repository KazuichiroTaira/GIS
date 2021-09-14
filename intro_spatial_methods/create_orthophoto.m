function []=create_orthophoto()
format long g %more decimals to console

laserdata=read_laserdata(); 
[pp_x,pp_y,c,R,X0,Y0,Z0]=read_camera_parameters();

%open image
image=imread('test_image_gray.tif');
imsize=size(image) %image dimensions (rows, columns)

%visualizing original image
figure(1)
imshow(image)
title('Original image') 

%initialize empty ortho image


grid_size=0.2; %grid size of ortho image

%todo: start with 3 pixel ortho image and check if your code is in
%condition:
%pixels_columns=3;
%pixels_rows=1

%when you have a functional code search for minumum and maximum values from laser data 
%and compute how many pixels you need for orthophoto
%when you have a functional code, replace this and compute how many pixels
%you need for your ortho image in order to cover the area that has laser points

%pixels_columns=
%pixels_rows=


orthophoto=zeros(pixels_rows, pixels_columns); %initializing final ortho image (gray-level: RGB should be ortho_image=zeros(pixels_rows, pixels_columns, 3);
DEM=zeros(pixels_rows, pixels_columns); %initializing digital elevation model
%ground coordinates of the starting pixel. Notice the growing direction of
%y

%todo:
%in the case of 3 pixels ortho image use:
%start_x=6111.4;
%start_y=5267;
%when you have a functional code replace this with minimum x value and
%maximum y value (think about the directions of coordinate axes in reality and in digital ortho image)
%start_x=
%start_y=

% Create a KD-tree for faster search of neighbors 
tree = KDTreeSearcher(laserdata(:,1:2));

%we go through all ortho image pixels and set a height to it

for i=1:pixels_rows
   for j= 1:pixels_columns
       %ground coordinates of current pixel center
       X=start_x+(j-1)*grid_size; 
       Y=start_y-(i-1)*grid_size; %notice the direction, because the coordinate systems of digital image (rows) and the ground Y are opposite 

       %find five closest points with a KD-tree
       [Idx,D] = knnsearch(tree, [X,Y], 'K', 5); 
       closest_5 = [D.', laserdata(Idx,:)];
       
       %apply IDW interpolation
       interpolated_height=inverse_distance_weighting_interpolation(X,Y,closest_5);
       
       %creating DEM
       DEM(i,j)=interpolated_height;
       
       %project all 3D grid points from empty orhto image into the aerial
       %image and interpolate the best color value
       
       [x_camera, y_camera]=collinearity_equations(X, Y, interpolated_height,  c, X0, Y0, Z0, R); %3D point to image plane
       
       [row,column]=camera_coordinates2image_coordinates(x_camera, y_camera, pp_x, pp_y); %from camera coordinate system into image coordinate system

       if row>1 && column>1 && row<imsize(1)+1 && column<imsize(2)+1 %floor cannot lead to 0... therefore >1
           %selecting the best color value from original image using
           %bilinear interpolation
            interpolated_color=uint8(bilinear_interpolation(column, row, double(image(floor(row),floor(column))), double(image(floor(row),ceil(column))), double(image(ceil(row),floor(column))), double(image(ceil(row),ceil(column)))));
            orthophoto(i,j)=interpolated_color; %setting interpolated color value to ortho image 

       else
           orthophoto(i,j)=0; %if we are outside the image area, set color value zero
       end
   end
end
%visualizing the results
figure(2)
im=imshow(mat2gray(orthophoto)); %mat2gray changes matrix into an image type
title('Orthophoto') 
%ortho_image

end

function [laserdata]=read_laserdata()
    laserdata=load('laserdata.txt'); %todo:check if you need path to file
end

function [pp_x,pp_y,c,R, X0,Y0,Z0]=read_camera_parameters()
    f=fopen('camera_orientation_info.txt'); %todo:check if you need a path to file
    line = fgets(f);%skip line
    
    %principle point
    line = fgets(f);
    pp_x = sscanf(line,'%f');
    line = fgets(f);
    pp_y = sscanf(line,'%f');
    
    line = fgets(f);%skip line
    
    %camera constant
    line = fgets(f);
    c = sscanf(line,'%f');
    
    line = fgets(f);%skip line
    line = fgets(f);%skip line
    line = fgets(f);%skip line
    line = fgets(f);%skip line
    
    %projection center
    line = fgets(f);
    X0 = sscanf(line,'%f');
    line = fgets(f);
    Y0 = sscanf(line,'%f');
    line = fgets(f);
    Z0 = sscanf(line,'%f');     
    
    line = fgets(f);%skip line
    
    %rotation matrix
    R=zeros(3,3);
    line = fgets(f);
    R(1,:)=sscanf(line,'%f %f %f'); 
    line = fgets(f);
    R(2,:)=sscanf(line,'%f %f %f');
    line = fgets(f);
    R(3,:)=sscanf(line,'%f %f %f');


    fclose(f);%close file
end

function [interpolated_height]=inverse_distance_weighting_interpolation(X,Y,closest_5)
%todo: write code for IDW according to equations 1a and 1b in the
%assignment instructions

end

function [x_camera, y_camera]=collinearity_equations(X, Y, Z, c, X0, Y0, Z0, R)
    %todo: write code for collinearity equations according to equation 3 in the
    %assignment instructions
    
end

function [row,column]=camera_coordinates2image_coordinates(x_camera, y_camera, pp_x, pp_y)
   %todo: write code for transformation according to equation 4 in the
    %assignment instructions
end

function [interpolated_color]=bilinear_interpolation(x_image, y_image, color1, color2, color3, color4)
    %color1 = row,column; color2=row,column+1; color3=row+1,column; color4=row+1,column+1  
    %todo: write code for bilinear interpolation according to equation 5 in the
    %assignment instructions

end

